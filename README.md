# Land-Use Area Calculations from Digitized Maps

## Use Keynote to Add Area Overlays

Use a unique color for each land-use type and include the map scale.  The resulting documents have two pages:
the first includes the scanned map in the background, and the second only shows the area overlays.

## Convert Keynote to PNG and Capture Metadata

* Export each keynote document to a 2-page PDF document.
* Open the PDF in Preview and Export to PNG at 300 pixels/inch.
* Open the PNG in Preview and use the cursor to measure the length of the map scale on the first page.
* Record the scale in the spreadsheet using the format `775px = 500m`.
* Re-open the PDF document and delete the first page then crop the second page. Re-export to PNG at 300 pixels/inch.
* Count the number of different colors and record this in the spreadsheet.

## Update the Maps Folder

* Copy the cropped PNG files to the `maps/` folder of this repository.
* Update the YAML file containing the metadata.
* Commit and push.

## Run the pixelcount program
