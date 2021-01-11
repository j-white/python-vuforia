


python-vuforia
==============

Module for interacting with the Vuforia Web Services API (VWS API)


## USAGE

 Add client with valid credentials here:

```python
def main():
    v = Vuforia(access_key="YOUR_KEY_HERE",
                secret_key="YOUR_KEY_HERE")
```


## ADD TARGET TO CLOUD DATABASE

```python
image_file = open('PATH_TO_IMAGE')
image = base64.b64encode(image_file.read())
metadata_file = open('PATH_TO_METADATAFILE')
metadata = base64.b64encode(metadata_file.read())
print v.add_target({"name": "IMAGE_NAME", "width":float(320), "image": image, "application_metadata": metadata, "active_flag": 1})
```

## UPDATE TARGET TO CLOUD DATABASE

```python
target_id = "TARGET_ID"
image_file = open('PATH_TO_IMAGE')
image = base64.b64encode(image_file.read())
metadata_file = open('PATH_TO_METADATAFILE')
metadata = base64.b64encode(metadata_file.read())
print v.update_target(target_id,{"name": "IMAGE_NAME", "width":float(320), "image": image, "application_metadata": metadata, "active_flag": 1})
```


## DELETE A TARGET

```python
target_id = "TARGET_ID"
print v.delete_target(target_id)
```

## GET TARGET BY TARGET-ID

```python
target_id = "TARGET_ID"
print v.get_target_by_id(target_id)
```

## GET ALL TARGETS FROM DATABASE

```python
for target in v.get_targets():
        print target
```

## GET A DATABASE SUMMARY REPORT

```python
print v.get_summary()
```


## CHECK FOR DUPLICATE TARGETS

```python
target_id = "TARGET_ID"
print v.get_duplicate_targets(target_id)
```

## GET ALL TARGET ID'S

```python
print v.get_target_ids()
``` 
