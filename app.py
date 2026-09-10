
# ============================================================
# E-COMMERCE DELIVERY TIME PREDICTION APPLICATION
# ============================================================

# Streamlit creates the web application interface
import streamlit as st

# pandas is used to create the one-row DataFrame
# that will be passed to the trained model
import pandas as pd

# joblib loads the saved machine-learning pipeline
import joblib

# Path is used to reliably locate model.pkl
from pathlib import Path


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

# Configure the browser tab and page width
st.set_page_config(
    page_title="E-Commerce Delivery Time Predictor",
    page_icon="📦",
    layout="centered"
)


# ------------------------------------------------------------
# LOCATE AND LOAD THE TRAINED MODEL
# ------------------------------------------------------------

# Find the exact folder containing app.py
BASE_DIR = Path(__file__).resolve().parent

# model.pkl must be stored in the same folder
MODEL_PATH = BASE_DIR / "model.pkl"


# Load the saved preprocessing + regression pipeline
# safely so the application does not fail silently.
try:

    model = joblib.load(MODEL_PATH)

except Exception as error:

    st.error(
        f"Unable to load the prediction model: {error}"
    )

    # Stop the application because predictions cannot
    # be generated without the trained model.
    st.stop()


# ------------------------------------------------------------
# APPLICATION HEADING
# ------------------------------------------------------------

st.title(
    "📦 E-Commerce Delivery Time Predictor"
)

st.write(
    """
    This application estimates the expected delivery time of an
    e-commerce order using order, package, warehouse, courier,
    traffic and shipping information.
    """
)

st.caption(
    "Prediction output is expressed in hours."
)


# ------------------------------------------------------------
# USER INPUT SECTION
# ------------------------------------------------------------

st.subheader(
    "Enter Order Details"
)


# Use two columns to keep the application compact
left_column, right_column = st.columns(2)


# ------------------------------------------------------------
# LEFT-SIDE INPUTS
# ------------------------------------------------------------

with left_column:

    # Product category is a nominal categorical predictor.
    product_category = st.selectbox(
        "Product Category",
        [
            "Electronics",
            "Fashion",
            "Home & Kitchen",
            "Beauty",
            "Books"
        ]
    )


    # Shipping mode is a nominal categorical predictor.
    shipping_mode = st.selectbox(
        "Shipping Mode",
        [
            "Standard",
            "Express",
            "Same-Day"
        ]
    )


    # Order value:
    # The valid business range used for this project is
    # approximately ₹300 to ₹15,000.
    order_value = st.number_input(
        "Order Value (₹)",
        min_value=300.0,
        max_value=15000.0,
        value=6000.0,
        step=100.0
    )


    # Package weight:
    # Restricted to the valid project range.
    package_weight = st.number_input(
        "Package Weight (kg)",
        min_value=0.1,
        max_value=15.0,
        value=3.0,
        step=0.1
    )


    # Warehouse distance:
    # Restricted to the intended range represented by
    # the valid generated observations.
    warehouse_distance = st.number_input(
        "Warehouse Distance (km)",
        min_value=15.0,
        max_value=950.0,
        value=800.0,
        step=10.0
    )


# ------------------------------------------------------------
# RIGHT-SIDE INPUTS
# ------------------------------------------------------------

with right_column:

    # Number of items is an integer between 1 and 10.
    items_in_order = st.number_input(
        "Items in Order",
        min_value=1,
        max_value=10,
        value=4,
        step=1
    )


    # Valid warehouse processing time used in this project.
    warehouse_processing_hours = st.number_input(
        "Warehouse Processing Hours",
        min_value=0.5,
        max_value=6.0,
        value=3.0,
        step=0.1
    )


    # Courier Load Index uses a 1-10 scale.
    courier_load_index = st.number_input(
        "Courier Load Index",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.1
    )


    # Traffic Index also uses a 1-10 scale.
    traffic_index = st.number_input(
        "Traffic Index",
        min_value=1.0,
        max_value=10.0,
        value=9.0,
        step=0.1
    )


# ------------------------------------------------------------
# CREATE MODEL INPUT
# ------------------------------------------------------------

# IMPORTANT:
# These column names exactly match the predictor names
# used while training the saved machine-learning pipeline.
#
# Each value is placed inside a list because we are creating
# one new observation/row.

input_data = pd.DataFrame(
    {
        "Order_Value": [
            order_value
        ],

        "Package_Weight_Kg": [
            package_weight
        ],

        "Warehouse_Distance_Km": [
            warehouse_distance
        ],

        "Items_in_Order": [
            items_in_order
        ],

        "Warehouse_Processing_Hours": [
            warehouse_processing_hours
        ],

        "Courier_Load_Index": [
            courier_load_index
        ],

        "Traffic_Index": [
            traffic_index
        ],

        "Product_Category": [
            product_category
        ],

        "Shipping_Mode": [
            shipping_mode
        ]
    }
)


# ------------------------------------------------------------
# PREDICTION
# ------------------------------------------------------------

st.markdown("---")


if st.button(
    "Predict Delivery Time",
    type="primary",
    use_container_width=True
):

    try:

        # Send the new order through the complete saved
        # preprocessing + Linear Regression pipeline.
        prediction = model.predict(
            input_data
        )[0]


        # Safety check:
        # delivery time cannot meaningfully be negative.
        if prediction <= 0:

            st.error(
                "The model generated an invalid non-positive "
                "delivery-time estimate."
            )

        else:

            # Display prediction prominently
            st.metric(
                label="Predicted Delivery Time",
                value=f"{prediction:.2f} hours"
            )


            # Provide the managerial interpretation required
            # by the assignment.
            st.info(
                f"""
                Based on the entered order and logistics conditions,
                the model estimates that this order will require
                approximately **{prediction:.2f} hours** for delivery.

                A manager can use this estimate for delivery planning,
                workload coordination and setting customer expectations.
                """
            )

    except Exception as error:

        # Clearly display any prediction failure rather than
        # allowing the application to fail silently.
        st.error(
            f"Prediction could not be generated: {error}"
        )


# ------------------------------------------------------------
# MODEL INFORMATION
# ------------------------------------------------------------

with st.expander(
    "About this prediction model"
):

    st.write(
        """
        The application uses a Multiple Linear Regression model.

        Numerical predictors:
        - Order Value
        - Package Weight
        - Warehouse Distance
        - Items in Order
        - Warehouse Processing Hours
        - Courier Load Index
        - Traffic Index

        Categorical predictors:
        - Product Category
        - Shipping Mode

        The saved model file contains both the preprocessing steps
        and the trained regression model, ensuring that new inputs
        are processed consistently with the training workflow.
        """
    )


# ------------------------------------------------------------
# COPYRIGHT
# ------------------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; font-size:0.82rem;">
        © 2026 Arin Bakshi. All Rights Reserved.<br>
        Unauthorized copying, modification, redistribution or
        commercial use of this project is prohibited without
        prior written permission.
    </div>
    """,
    unsafe_allow_html=True
)
