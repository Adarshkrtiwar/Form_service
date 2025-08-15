from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.submission_model import SubmissionModel
from ..models.form_model import FormSchemaModel
from ..services.condition_parser import ConditionParser
from ..schemas.form_schema import FormSchema, FormField, FieldType

class SubmissionService:
    def __init__(self, db: Session):
        self.db = db
        self.condition_parser = ConditionParser()

    def submit_form(self, schema_id: str, answers: Dict[str, Any], client_ip: str, user_agent: str) -> Dict[str, Any]:
        # Get the schema
        schema = self.db.query(FormSchemaModel).filter(FormSchemaModel.id == schema_id).first()
        if not schema:
            raise ValueError("Schema not found")
        
        form_schema = FormSchema.parse_raw(schema.schema_json)
        
        # Validate and compute fields
        computed_fields = {}
        errors = {}
        
        for card in form_schema.cards:
            for field in card.fields:
                # Skip validation if field is not visible
                if field.visible_if and not self.condition_parser.evaluate(field.visible_if, answers):
                    continue
                
                # Handle computed fields
                if field.type == FieldType.COMPUTED and field.computation:
                    try:
                        computed_value = self._compute_field(field.computation, answers)
                        computed_fields[field.id] = computed_value
                    except Exception as e:
                        errors[field.id] = f"Computation error: {str(e)}"
                    continue
                
                # Validate required fields
                if field.validation and field.validation.required and field.id not in answers:
                    errors[field.id] = "This field is required"
                    continue
                
                # Validate field value if present
                if field.id in answers:
                    field_errors = self._validate_field(field, answers[field.id])
                    if field_errors:
                        errors[field.id] = field_errors
        
        if errors:
            raise ValueError({"errors": errors})
        
        # Store submission
        submission = SubmissionModel(
            schema_id=schema_id,
            payload=str(answers),
            computed_fields=str(computed_fields),
            status="accepted",
            client_ip=client_ip,
            user_agent=user_agent
        )
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        
        return {
            "submission_id": submission.id,
            "status": "accepted",
            "computed": computed_fields
        }

    def _validate_field(self, field: FormField, value: Any) -> Optional[str]:
        if not field.validation:
            return None
        
        validation = field.validation
        
        # Type-specific validation
        if field.type == FieldType.EMAIL:
            if "@" not in value:
                return "Invalid email format"
        
        # Length validation
        if isinstance(value, str):
            if validation.min_length and len(value) < validation.min_length:
                return f"Minimum length is {validation.min_length}"
            if validation.max_length and len(value) > validation.max_length:
                return f"Maximum length is {validation.max_length}"
        
        # Value validation for numbers
        if field.type == FieldType.NUMBER and isinstance(value, (int, float)):
            if validation.min_value is not None and value < validation.min_value:
                return f"Minimum value is {validation.min_value}"
            if validation.max_value is not None and value > validation.max_value:
                return f"Maximum value is {validation.max_value}"
        
        # Pattern validation
        if validation.pattern:
            import re
            if not re.match(validation.pattern, str(value)):
                return "Value does not match required pattern"
        
        # LOV validation
        if field.options:
            valid_values = [option["value"] for option in field.options]
            if str(value) not in valid_values:
                return f"Value must be one of: {', '.join(valid_values)}"
        
        return None

    def _compute_field(self, computation: str, answers: Dict[str, Any]) -> Any:
        # Very simple computation - only supports string concatenation for now
        if computation.startswith("$.firstName + ' ' + $.lastName"):
            return f"{answers.get('firstName', '')} {answers.get('lastName', '')}"
        raise ValueError("Unsupported computation")