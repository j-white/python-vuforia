python-vuforia
==============

Module for interacting with the Vuforia Web Services API (VWS API)

## USAGE

 // Add client with valid credentials here:

def main():
    v = Vuforia(access_key="YOUR_KEY_HERE",
                secret_key="YOUR_KEY_HERE")

// TO RUN 

python vuforia.py

## ADD TARGET TO CLOUD DATABASE

image_file = open('PATH_TO_IMAGE')
image = base64.b64encode(image_file.read())
metadata_file = open('PATH_TO_METADATAFILE')
metadata = base64.b64encode(metadata_file.read())
print v.add_target({"name": "IMAGE_NAME", "width":float(320), "image": image, "application_metadata": metadata, "active_flag": 1})

## UPDATE TARGET TO CLOUD DATABASE

target_id = "TARGET_ID"
image_file = open('PATH_TO_IMAGE')
image = base64.b64encode(image_file.read())
metadata_file = open('PATH_TO_METADATAFILE')
metadata = base64.b64encode(metadata_file.read())
print v.update_target(target_id,{"name": "IMAGE_NAME", "width":float(320), "image": image, "application_metadata": metadata, "active_flag": 1})


## DELETE A TARGET

target_id = "TARGET_ID"
print v.delete_target(target_id)

## GET TARGET BY TARGET-ID

target_id = "TARGET_ID"
print v.get_target_by_id(target_id)

## GET ALL TARGETS FROM DATABASE

for target in v.get_targets():
        print target

## GET A DATABASE SUMMARY REPORT

print v.get_summary()


## CHECK FOR DUPLICATE TARGETS

target_id = "TARGET_ID"
print v.get_duplicate_targets(target_id)

## GET ALL TARGET ID'S

print v.get_target_ids()   
