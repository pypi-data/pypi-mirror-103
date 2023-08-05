from typing import Dict, List, Any


def validate(schema: Dict[str, Any], records: List[Dict[str, Any]]):
    result = []
    for record in records:
        item = {}
        for field, validator in schema.items():
            required, value = field[0] == '*', None
            field = field[1:] if required else field
            for key in reversed(field.split(':=')):
                value = record.get(key, value)

            if required and value is None:
                raise ValueError(f'The field "{key}" is required.')

            if value is not None:
                if isinstance(validator, dict):
                    item[key] = next(iter(
                        validate(validator, [value])))
                    continue
                elif isinstance(validator, list):
                    validator = validator.pop()
                    if isinstance(validator, dict):
                        item[key] = validate(validator, value)
                    else:
                        item[key] = [validator(item) for item in value]
                    continue

                outcome = validator(value)
                if isinstance(outcome, Exception):
                    raise outcome

                item[key] = outcome

        result.append(item)

    return result
