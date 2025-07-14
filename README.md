---
title: FungiSage Vision (Gradio UI)
emoji: 🍄🤖
colorFrom: gray
colorTo: pink
sdk: gradio
sdk_version: 5.36.2
app_file: src/app.py
pinned: false
license: apache-2.0
short_description: "Powered by musheff: AI that knows its fungi."
tags:
  - gradio
  - vision
  - mushroom
  - musheff
datasets:
  - SoFa325/12_popular_russia_mushrooms_edible_poisonous
models:
  - blasisd/musheff
---

# FungiSage Vision: Where data meets delicious—or dangerous

FungiSage Vision transforms foraging into a safe, science-backed adventure. Powered by our [`musheff`](https://huggingface.co/blasisd/musheff) model (a fine-tuned EfficientNet-B3 trained on _SoFa325/12_popular_russia_mushrooms_edible_poisonous_), it identifies 12 common Russian species in seconds—delivering instant edibility/toxicity alerts with the solid reliability of a mountain massif. Snap a photo, and forage with AI-powered confidence.

## Getting Started

This guide provides step-by-step instructions to set up and run the project on your local machine for development and testing purposes. For details on deploying the project to a production environment, refer to the Deployment section.

### Prerequisites

To set up and run this project, ensure the following software and tools are installed on your system:

- **Python**: Version `3.10.12` or higher is required. Verify your Python version by running:

  ```bash
  python3 --version
  ```

- **Dependencies**: Install the required Python packages listed in requirements.txt using pip. Run the following command in your terminal:

  ```bash
  pip install -r requirements.txt
  ```

- **Backend server**: This project is the frontend component only. Before proceeding, ensure you've deployed the backend server:

  1. **Deploy the backend:**
     - Implementation → [blasisd/musheff-api](https://huggingface.co/spaces/blasisd/musheff-api/tree/main).
  2. **Configure environment variable:**

     - Set `MUSHEFF_API_BASE_URL` variable in your environment to your backend's root URL:

       ```bash
       MUSHEFF_API_BASE_URL="https://your-backend-server.com"  # No trailing slash!
       ```

### Local Development and Testing

To run the application locally for development and testing purposes, execute the following command in your terminal:

```bash
python app.py
```

> [!WARNING]
> Ensure you are in the project's **src** directory before running the script or adapt running path.

## Deployment

### Deployment on Hugging Face Spaces

To deploy the project on Hugging Face Spaces, follow these steps:

1. Create an account on [Hugging Face](https://huggingface.co) if you don’t already have one.

2. Refer to the official [Spaces Overview](https://huggingface.co/docs/hub/en/spaces-overview) documentation for detailed instructions on setting up and deploying your project.

### Deployment on Other Cloud Platforms

For deployment on other cloud or live systems, consult the documentation provided by your chosen service provider. Each platform may have specific requirements and steps for deploying Python-based applications.

## Built With

- [Python 3.10.12](http://www.python.org/) - Developing with the best programming language

## Authors

**Vlasios Dimitriadis** - _Initial work:_ [FungiSage Vision](https://huggingface.co/spaces/blasisd/fungi-sage-vision)
