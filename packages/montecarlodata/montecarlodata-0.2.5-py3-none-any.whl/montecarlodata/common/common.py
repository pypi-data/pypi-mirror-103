from typing import Optional


def normalize_gql(field: str) -> Optional[str]:
    if field:
        return field.replace('_', '-').lower()
