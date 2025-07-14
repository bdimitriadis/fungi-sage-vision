import os
from typing import Any

import gradio as gr
import requests

from dotenv import load_dotenv


load_dotenv()


API_ENDPOINT = f"{os.getenv('MUSHEFF_API_BASE_URL')}/classify"


def classify_image(img_path: str) -> tuple[dict[str, Any]]:
    """Classifies a mushroom image, returning species, edibility, and confidence score.
    In case of error returns the error.

    :param img_path: the path to the mushroom image
    :type img_path: str
    :return: confidence score, species, edibility or error message (as output or error components)
    :rtype: tuple[dict[str, Any]]
    """
    try:
        with open(img_path, "rb") as fp:
            files = {"image_file": (fp.name, fp)}

            # Calling the service
            response = requests.post(API_ENDPOINT, files=files)

            # Handle HTTP errors
            if response.status_code != 200:
                error_msg = response.json().get(
                    "detail", f"API Error {response.status_code}"
                )
                return show_error(f"Backend Error: {error_msg}")

            # Process successful response
            data = response.json()
            return show_results(data)

    except requests.exceptions.Timeout:
        return show_error("Request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        return show_error("Cannot connect to the server. Please check your connection.")
    except TypeError:
        return show_error("Invalid input. Please select a valid file and try again.")
    except Exception as e:
        return show_error(f"System error: {e}")


def show_results(data: dict) -> tuple[dict[str, Any]]:
    """Show the results data retrieved from the service
    in the respective output components

    :param data: the data retrieved from the classify service
    :type data: dict
    :return: the output components
    :rtype: tuple[dict[str, Any]]
    """

    # Create visual output components
    confidence = data["confidence"]
    class_name = data["mushroom_type"]
    edibility = data["toxicity_profile"]

    return (
        # Confidence output
        gr.update(
            value=generate_confidence_html(confidence),
        ),
        # Species display
        gr.update(
            value=generate_class_html(class_name),
        ),
        # Edibility alert
        gr.update(
            value=generate_edibility_html(edibility, confidence, class_name),
        ),
        gr.update(value=""),  # Error output
    )


def show_error(message: str) -> tuple[dict[str, Any]]:
    """Update the error output component with the error message
    Nullify all the other output components

    :param message: the error message
    :type message: str
    :return: the error message component, along with the other nullified output components
    :rtype: tuple[dict[str, Any]]
    """
    return (
        gr.update(value=""),  # Confidence output
        gr.update(value=""),  # Class output
        gr.update(value=""),  # Edibility output
        gr.update(value=generate_error_html(message)),  # Error alert
    )


def generate_confidence_html(confidence):
    return f"""<div class="confidence-display" style="font-size:1.1rem">
        <div class="confidence-header">
            <span class="confidence-icon">📊</span>
            <span class="confidence-title">Classification Confidence</span>
        </div>

        <div class="confidence-visual">
            <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width: {confidence*100:.2f}%"></div>
            </div>
            <div class="confidence-value">{confidence*100:.2f}%</div>
        </div>
    </div>
    """


def generate_class_html(class_name):
    return f"""
    <div style='
        font-size: 1.5rem;
        text-align: center;
        padding: 20px;
        background: #E3F2FD;
        border-radius: 8px;
    '>
        🍄 <br><strong>{class_name.replace("_", " ")}</strong>
    </div>
    """


def generate_edibility_html(edibility, confidence, class_name):
    if edibility == "edible":
        return (
            f"<div class='edible-alert'>"
            f"✅ SAFE TO EAT (with verification)<hr style='margin:10px 0;'>"
            f"<div style='font-size:1.1rem'>"
            f"Always confirm with mycologist before consumption"
            f"</div></div>"
        )
    else:
        return (
            f"<div class='poison-alert'>"
            f"☠️ <strong>POISONOUS!</strong> DO NOT CONSUME<hr style='margin:10px 0;'>"
            f"<div style='font-size:1.1rem;color:var(--poison-color)'>"
            f"Misidentification risk: {100 - confidence*100:.2f}%<br>"
            f"<em>Immediately contact poison control if ingested</em>"
            f"</div></div>"
        )


def generate_error_html(message):
    return f"""
    <div class='error-banner'>
        <span class='error-icon'>❌</span>
        <strong>CLASSIFICATION FAILED</strong><br>
        {message}<br>
        <em>Please try again or contact support</em>
    </div>
    """


def toggle_row_visibility(*comp_vals):
    """Update row visibility based on non empty value(s) of component(s) on row"""
    return gr.Row(visible=any(comp_vals))


def handle_image_change(new_image):
    """This function will be called when image changes (cleared or new one selected)"""
    # New image selected or deleted (new_image or None), in any case reset output components
    return (
        new_image,
        gr.Row(visible=False),
        gr.Row(visible=False),
        gr.update(visible=False),
    )


def hr_line_update():
    return gr.update(visible=True)


# Custom HTML components
safety_html = """
<div class="safety-banner">
    <div class="warning-icon">⚠️</div>
    <strong>CRITICAL SAFETY NOTICE:</strong> FungiSage Vision provides probabilistic guidance only - not guarantees.
    Mushroom misidentification can be fatal. Always consult certified mycologists before consumption.
</div>
"""

slogan_html = """
<div class="slogan-container">
    <div class="mushroom-icon">🍄</div>
    <div class="slogan-text">
        <span class="brand-tagline">Massif Mushroom Intelligence.</span>
        <div class="brand-action">
            <span class="brand-name">FungiSage Vision</span> Guides,
            <span class="verify-emphasis">You Verify.</span>
        </div>
    </div>
</div>
"""

# CSS file path
css_path = os.path.join(os.path.dirname(__file__), "static/styles/custom.css")

with gr.Blocks(
    theme=gr.themes.Glass(),
    css_paths=css_path,
) as demo:
    gr.HTML(safety_html)
    gr.HTML(slogan_html)

    # Input section
    with gr.Group(elem_id="inputsContainer"):
        gr.Markdown("### Upload Mushroom Image", elem_id="uploadHeader")
        image_input = gr.Image(type="filepath", label="", height=300)
        classify_btn = gr.Button(
            "Classify Mushroom", elem_id="classifyBtn", variant="primary"
        )

    # Output section
    with gr.Group(elem_id="outputsContainer"):
        with gr.Row(visible=False, scale=1, equal_height=True) as results_group:
            with gr.Column(scale=1, elem_id="confCol"):
                confidence_output = gr.HTML(
                    label="Confidence Level", elem_classes="output-card"
                )

            with gr.Column(scale=2, elem_id="speciesCol"):
                class_output = gr.HTML(
                    label="Identified Species", elem_classes="output-card"
                )

            with gr.Column(scale=1, elem_id="edibilityCol"):
                edibility_output = gr.HTML(
                    label="Safety Assessment", elem_classes="output-card"
                )

        with gr.Row(visible=False) as errors_group:
            error_output = gr.HTML(elem_classes="error-card")

        # Used only for auto scrolling when results or errors occur
        bottom_line = gr.HTML("<hr>", visible=False, elem_id="bottomLine")

    # Classification function called on button click
    classify_btn.click(
        fn=classify_image,
        inputs=image_input,
        outputs=[
            confidence_output,
            class_output,
            edibility_output,
            error_output,
        ],
    ).then(
        fn=toggle_row_visibility,
        inputs=[confidence_output, class_output, edibility_output],
        outputs=results_group,  # If any of the result outputs (got results from service), then show results row
    ).then(
        fn=toggle_row_visibility,
        inputs=[error_output],
        outputs=errors_group,  # If error occurred, then show errors row
    ).then(
        fn=hr_line_update,
        inputs=[],
        outputs=[bottom_line],
        scroll_to_output=True,  # Useful to scroll there after results or errors occur
    )

    # Handle image changes (upload or clear/hide rows with results and errors)
    image_input.change(
        fn=handle_image_change,
        inputs=image_input,
        outputs=[image_input, results_group, errors_group, bottom_line],
    )


if __name__ == "__main__":
    demo.launch()
