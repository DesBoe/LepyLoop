# LEPYLoop

![LEPYLOOP Logo](./Logo.png)

**LEPYLoop** is a tool to automate the analysis of large numbers of images with [LEPY](https://github.com/tzlr-de/LEPY). LEPY can also be used without LEPYLoop.

---

**Background**

Please read the deocumentation of [LEPY](https://github.com/tzlr-de/LEPY).

LEPY can process many images, but may hit hardware limits with very large datasets. LEPYLoop is a workaround to overcome these limitations.


---

## Idea

LEPYLoop splits large image sets into small packages, which are then analyzed one after another by LEPY. After analysis, all images are restored to their original locations and the outputs are organized.

---

## Preparation

- Place all moth images in a folder (subfolders are supported).
- If you have RGB and UV images of the same moth, you can use **LLCheck** to find missing or unmatched images.

---

## Execution

### Environment

1. Start your Anaconda environment with LEPY installed.
2. Change to the directory containing LEPY's `main.py`.
3. Start LEPYLoop with:

	 ```bash
	 python3 /path/to/LLmain.py
	 ```

### Settings

Before starting, LEPYLoop will ask for the following settings:

- **Input directory:**
	- The folder containing the images to be analyzed (subfolders are supported).
	- All images will be moved into a single "input" folder.

- **Mode:**
	- `rgb`: Only RGB images
	- `uv`: Matching UV images are provided

- **Number of individuals per run:**
	- Recommendation: 100 (try a lower number if you experience issues)

- **Export as JPG:**
	- TIFF images can be exported as JPG for better usability (type in "yes" or "no")

- **Corrected data (rePoint):**
	- If you have corrected results with the rePoint tool, you can re-analyze them ("yes" or "no").
	- If "yes", you must provide the path to the JSON file containing the corrected POI data.

---
## rePOInt
You can download rePOInt tool on GitHub:
[rePOInt tool (GitHub)](https://github.com/DiKorsch/rePOInt)
---


### LEPY only
A full documentation on LEPY can be found at:
[LEPY (GitHub)](https://github.com/tzlr-de/LEPY)

```bash
./main.py /path/to/images config.yml
```

---

## References

**Publication:**  
LEPY was described by Correa-Carmona et al. (submitted). A preprint is available:  
[Preprint (bioRxiv)](https://doi.org/10.32942/X2WS78)

**Validation Data:**  
[Validation Data (GitHub)](https://github.com/YennyCC/LEPY_Suplementary_Files.git)

**LEPY Download:**  
[LEPY Repository (GitHub)](https://github.com/tzlr-de/LEPY.git)

## Operating Systems

Tested on **macOS 15.1** and **Python 3.12.0**

**Note for Windows users:**

Please go to "Start → Settings → App execution aliases" and turn off the entries for `python.exe` and `python3.exe`.