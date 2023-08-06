from invoke import Collection
from outcome.utils import env

from outcome.devkit.invoke.tasks import check, clean, database, pact, release, setup, test

namespace = Collection(setup, clean, release, check, test, database, pact)

namespace.configure({'run': {'echo': True, 'pty': not env.is_ci()}})
