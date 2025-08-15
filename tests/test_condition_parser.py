from app.services.condition_parser import ConditionParser

def test_simple_condition():
    parser = ConditionParser()
    data = {"field1": "value1", "field2": "value2"}
    
    assert parser.evaluate("$.field1 == 'value1'", data) == True
    assert parser.evaluate("$.field1 != 'value2'", data) == True
    assert parser.evaluate("$.field2 == 'value1'", data) == False

def test_and_condition():
    parser = ConditionParser()
    data = {"field1": "value1", "field2": "value2"}
    
    assert parser.evaluate("$.field1 == 'value1' and $.field2 == 'value2'", data) == True
    assert parser.evaluate("$.field1 == 'value1' and $.field2 == 'wrong'", data) == False

def test_or_condition():
    parser = ConditionParser()
    data = {"field1": "value1", "field2": "value2"}
    
    assert parser.evaluate("$.field1 == 'wrong' or $.field2 == 'value2'", data) == True
    assert parser.evaluate("$.field1 == 'wrong' or $.field2 == 'wrong'", data) == False