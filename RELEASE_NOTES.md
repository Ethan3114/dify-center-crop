# Center Crop v0.0.3

Fix Dify Cloud package parsing by normalizing the author identifier to lowercase `ethan3114`. The GitHub repository owner remains `Ethan3114`.

Version 0.0.2 was rejected by the live cloud installer with `plugin_unique_identifier is not valid` because the author identifier contained an uppercase letter. Version 0.0.3 retains the same center-crop behavior: by default preserve the central 85% of both width and height, without resizing or padding.

Validation: official CLI packaging, the runtime identifier format, Python 3.12 SDK configuration loading and PNG tool output. Cloud installation and Agent invocation are being tested and should only be considered verified once live checks pass.

The package is unsigned and has not been reviewed by Dify Marketplace.
