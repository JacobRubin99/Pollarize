# Pollarize

## Check It Out
[pollarize.us](http://pollarize.us)


## Development

### Database Migration
1. Modify models.py
2. Run `flask db migrate -m "NAME_OF_MIGRATION"` in `app/` directory.
3. Observe that new `app/migrations/versions/*.py` migration has been created.
4. If good to go, run `flask db upgrade` to bring database up to date.

### Database Connection
Create a file under `app/` called `config.py` with variable e.g. `SQLALCHEMY_DATABASE_URI="postgresql://user:pass@host:5432"`

### Redoing Choice ID

1. run "dropdb pollarize"
2. run "createdb pollarize"
3. run "flask db upgrade"

### Populating Poll and Choice Data

INSERT INTO Profile (id) VALUES (1) ON CONFLICT DO NOTHING;

COPY Poll(id, title, date_added, creator_user_id)
FROM '/home/vcm/cs316/pollarize/pollData.csv'
DELIMITER ','
CSV HEADER;

COPY Choice(poll_id, title, date_added, creator_user_id, rating)
FROM '/home/vcm/cs316/pollarize/choiceData.csv'
DELIMITER ','
CSV HEADER;

### Adding Trigger to PSQL

CREATE FUNCTION update_votes() RETURNS 
TRIGGER AS $$
BEGIN
UPDATE Choice SET Rating = Rating + NEW.value WHERE Choice.id = NEW.choice_id;
RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER voteTrigger
AFTER INSERT OR UPDATE
ON Vote
FOR EACH ROW
EXECUTE PROCEDURE update_votes();


