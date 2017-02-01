# ShadowDjangoUtils - Utilities for Django Applications

I found myself using the same "helper" code across multiple Django apps.

As such, I've split it out into its own library; as I continue to use the
library, it will receive updates that supplement my needs, and/or community
contributions.

## Installation and Usage

Clone the repository into your Django installation folder, along with your other
apps. Then simply `import shadowdjangoutils`.

## Contributing

If you have a feature you want to see, or a bug you can fix, send a pull
request; contributions become part of the project in accordance with the project
license (currently GNU LGPL - see the LICENSE.md file for details).

## Examples

#### ChoicesEnum + ValidatedModel

    from django.db import models
    from uuid import uuid4
    from django.core.validators import validate_slug as slug
    from shadowdjangoutils import ChoicesEnum, ValidatedModel

    class Game(ValidatedModel):

        # choices object can be inside or outside of model class
        GState = ChoicesEnum([
            ('finished',   0),
            ('lobby',      1),
            ('beginRound', 2),
            ('midRound',   3),
        ])

        uuid        = models.UUIDField(primary_key=True, default=uuid4)
        title       = models.CharField(max_length=20)
        url         = models.CharField(
            max_length=20, blank=True, validators=[slug])
        gamestate   = models.PositiveSmallIntegerField(
            choices=GState.choices(), default=GState.lobby)

        def clean(self):
            # unique game URLs where the game is in progress
            # but may clash with a previous game
            # GState.finished is no-longer-active, hence excluded

            if self.gamestate!=GState.finished and self.url!="":
                sameurl = self.__class__.objects.filter(
                    url=self.url).exclude(
                    gamestate=GState.finished, uuid=self.uuid)

                if sameurl.exists():
                    self.addErr((
                        "URL handle \"{0.url}\" is not unique (in current "+
                        "games)").format(self), field="url")
