# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

PRODUCT_NAME = Express
PRODUCT_VERSION = 3.1
UI_VERSION = 3.1

PRODUCT_EXTRA = -SP5

BASENAME = $(PRODUCT_NAME)-$(PRODUCT_VERSION)
REVISION = polar


# - NAME, VERSION and UI_VERSION: meaning should be fairly obvious
# - PRODUCT_EXTRA: provides post-release service pack sequencing
#   (-SP1, -SP2, etc.)
# - BASENAME: provides part of the ISO file name; it is usually
#   $(NAME)-$(VERSION), but will have a suffix for all ISOs *but*
#   the initial release.
# - REVISION: contains the code name for the actual release
#   (degu, polar, orca, etc.) and indicates pre-release
#   development progress (-alaph, -beth, -gamal, -rc1, -rc2, etc.)

# During development, clear PRODUCT_EXTRA and set BASENAME and
#   REVISION accordingly.

# For final release, clear PRODUCT_EXTRA, set REVISION to
#   the release's code name, and delete the development suffix
#   from BASENAME.

# For service packs, set PRODUCT_EXTRA to the -SP suffix
#   and set REVISION to the release's code name.

# Examples:
# PRODUCT_EXTRA =
# BASENAME = $(PRODUCT_NAME)-$(PRODUCT_VERSION)-dalat
# REVISION = polar-dalat
# 
# PRODUCT_EXTRA =
# BASENAME = $(PRODUCT_NAME)-$(PRODUCT_VERSION)
# REVISION = polar
# 
# PRODUCT_EXTRA = -SP3
# BASENAME = $(PRODUCT_NAME)-$(PRODUCT_VERSION)
# REVISION = polar
