"""
Additive schema upgrades, since the project has no migration tool.

create_all() only creates missing tables; upgrade_schema() also adds the
columns models gained after their table was created, and widens VARCHAR
columns that became TEXT. It never drops, renames or narrows anything, so
it is safe to run on every deploy (app/scripts/init_db.py does).
"""
from sqlalchemy import inspect, text, Text, String
from sqlalchemy.schema import CreateColumn


def upgrade_schema(db):
    """Bring the database up to the models. Returns a list of the changes made."""
    db.create_all()

    engine = db.engine
    inspector = inspect(engine)
    quote = engine.dialect.identifier_preparer.quote
    changes = []

    with engine.begin() as conn:
        for table in db.metadata.sorted_tables:
            existing = {col['name']: col for col in inspector.get_columns(table.name)}
            for column in table.columns:
                current = existing.get(column.name)
                if current is None:
                    ddl = CreateColumn(column).compile(dialect=engine.dialect)
                    conn.execute(text(f'ALTER TABLE {quote(table.name)} ADD COLUMN {ddl}'))
                    changes.append(f'added {table.name}.{column.name}')
                elif _needs_widening(current['type'], column.type) and engine.dialect.name == 'mysql':
                    # SQLite doesn't enforce VARCHAR lengths, so only MySQL needs this.
                    ddl = CreateColumn(column).compile(dialect=engine.dialect)
                    conn.execute(text(f'ALTER TABLE {quote(table.name)} MODIFY COLUMN {ddl}'))
                    changes.append(f'widened {table.name}.{column.name} to TEXT')
    return changes


def _needs_widening(db_type, model_type):
    return isinstance(model_type, Text) and isinstance(db_type, String) and not isinstance(db_type, Text)
