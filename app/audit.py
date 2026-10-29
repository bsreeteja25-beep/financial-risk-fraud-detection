from sqlalchemy.orm import Session
from app.models import AuditLog

def log_action(db: Session, action: str, resource_type: str, resource_id=None,
               actor: str = "api-user", details: str | None = None):
    db.add(AuditLog(action=action, resource_type=resource_type,
                    resource_id=str(resource_id) if resource_id is not None else None,
                    actor=actor, details=details))
