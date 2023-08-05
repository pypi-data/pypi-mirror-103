import mimetypes

from pathlib import Path
from organize.utils import DotDict, flatten

from .filter import Filter


class MimeType(Filter):

    """
    Filter by MIME type associated with the file extension.

    Supports a single string or list of MIME type strings as argument.
    The types don't need to be fully specified, for example "audio" matches everything
    from "audio/midi" to "audio/quicktime".

    You can see a list of known MIME types on your system by running this oneliner:

    .. code-block:: yaml

      python3 -c "import mimetypes as m; print('\\n'.join(sorted(set(m.common_types.values()) | set(m.types_map.values()))))"


    Examples:
        - Show MIME types:

          .. code-block:: yaml
            :caption: config.yaml

            rules:
              - folders: '~/Downloads'
                filters:
                  - mimetype
                actions:
                  - echo: '{mimetype}'

        - Filter by "image" mimetype:

          .. code-block:: yaml
            :caption: config.yaml

            rules:
              - folders: '~/Downloads'
                filters:
                  - mimetype: image
                actions:
                  - echo: This file is an image: {mimetype}

        - Filter by specific MIME type:

          .. code-block:: yaml
            :caption: config.yaml

            rules:
              - folders: '~/Desktop'
                filters:
                  - mimetype: application/pdf
                actions:
                  - echo: 'Found a PDF file'

        - Filter by multiple specific MIME types:

          .. code-block:: yaml
            :caption: config.yaml

            rules:
              - folders: '~/Music'
                filters:
                  - mimetype:
                    - application/pdf
                    - audio/midi
                actions:
                  - echo: 'Found Midi or PDF.'
    """

    def __init__(self, *mimetypes):
        self.mimetypes = list(map(str.lower, flatten(list(mimetypes))))

    @staticmethod
    def mimetype(path):
        type_, _ = mimetypes.guess_type(path, strict=False)
        return type_

    def matches(self, path: Path):
        mimetype = self.mimetype(path)
        if mimetype is None:
            return False
        if not self.mimetypes:
            return True
        return any(mimetype.startswith(x) for x in self.mimetypes)

    def pipeline(self, args: DotDict):
        if self.matches(args.path):
            result = self.mimetype(args.path)
            return {"mimetype": result}
        return None

    def __str__(self):
        return "MimeType(%s)" % ", ".join(self.mimetypes)
