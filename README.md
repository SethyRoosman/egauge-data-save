# Storing eGauge Waveform Data in .csv files
This program uses the eGauge Python API to scrape waveform data from the eGauge's registers. After scraping, the data is written to a .csv file and stored into a data_files subdirectory.
---

Install the prerequisite libraries
```bash
pip3 install egauge-python
pip3 install plotly==5.16.1
```

Fill out the config.json file with your eGauge's information
```bash
{
	"URI": "https://EGAUGEHOSTNAME.egaug.es",
	"USR": "USERNAME",
	"PWD": "PASSWORD",
	"DUR": 0.034
}
```
---
after running:

![example-run](https://user-images.githubusercontent.com/41768574/262707019-12da8c70-0749-4ad3-ae2d-5f32b3334068.png)