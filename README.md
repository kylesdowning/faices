# faices
## Contributors: Charlie Laursen, Kyle Downing

Class project for **Privacy Enhancing Technologies** (CSCI-497) at Western Washington University. 

Analysis of facial recognition and verification systems on AI generated facial images.

---

## About

Facial recognition is increasingly used as a trusted method to identify individuals. Facial recognition is used in many applications, including authentication for unlocking personal devices or in identifying individuals in digital images. Simultaneously, we have seen the quality of Artificial Intelligence systems increase and these systems become more widely available to the general public. 

With the ability to recreate a person's face digitally, people could use AI generated images of real faces in an effort to create fraudulent media to tarnish a person's identity. People generally speculate about whether digital media being AI generated, but sometimes cannot determine with absolute certainty. 

Given the multiple instances of ongoing or future privacy violations, our project scope is generalized to focus on the question of the susceptibility of facial recognition models against AI generated faces. We will look at face verification between a set of AI generated faces and real faces, and between a set of real faces and AI generated faces. In the first scenario, we will look to answer whether facial recognition models trained on synthetic face data neutralize privacy protections such as Fawkes. In the second scenario, we will answer whether AI generated facial images produce sufficiently similar embeddings to real faces to the point where they can pass verification against facial recognition systems.

---

## Disclaimer

Our repo contains multiple directories with hundreds of images. Overall, this project will take up a lot of space and require even more in order to install dependencies. The python program will allow you to preform operations on the dataset, which were created by us during the process of creating these datasets. The functions are not currently grouped and require manual inspection in order to preform the expected operation. In other words, some functions are used for mass file operations and others are used for analysis with **DeepFace**.

---

## Project Code

All code for the project is organized under the **src** directory. We used **python** as our langauge of choice, due to the great level of support for libraries that would be essential for this project. We used **uv** as our python package manager, and highly reccomend also using it when running this code.

To run the python program, make sure you use the following command before to install dependices:

```
uv sync
```

Then to run the program use:

```
uv run python main.py
```

We recognize there is not a high requirement in order to run the code for our project. Most of the code we developed was directly used for processing and creating our datasets, and leftover as an artifact to satisfy our requirement for a built component. In our paper, we discuss this further in detail and reccomend future development go towards a user-centered application which will utilize the Fawkes tool creating a more accessible and usable interface.

---

## Project Artifacts

The datasets we gathered and processed for our project is available on this directory. The final data analysis and processing for our results was done seperately on [Google Sheets](https://docs.google.com/spreadsheets/d/1N39Xokwnqrs3_SHyLGpE1A81fXSeJ4gRx293ymM1d7Y/edit?usp=sharing). 

Since the naming of our directories may be confusing, we provided a guide to which images are in each directory and which step they represent in our research process.

1. **images**: This is the original dataset we collected from the [UTXFace dataset](https://susanqq.github.io/UTKFace/). We cleaned the entries in this dataset to match the number of entries in every other dataset for simplicity. The images we removed were ones that were not successfully processed by DeepFace often due to no face being recognized. We ran into this issue later in our analysis, which we dive deeper into in our paper.
2. **images-cloaked-low**, **images-cloaked-med**: These directories contain the images processed by fawkes at the low and medium settings. Fawkes allows three levels of processing (low, mid, high). We decided to not include high processing images as the processing time was excessive.
3. **results**: This contains the final CSV file with the distance results from our final analysis. 

---

## Other Components

Our project uses Fawkes for image cloaking. However, we only found this tool to be usable from downloading the binary off of their [official website](https://sandlab.cs.uchicago.edu/fawkes/). If you would like to recreate this experiment, we highly reccomend following that route and researching the CLI use of the tool.
