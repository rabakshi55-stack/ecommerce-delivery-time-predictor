
# Import Streamlit for creating the interactive web application
import streamlit as st

# Import pandas for creating the single-row DataFrame
# that will be passed to the trained model
import pandas as pd

# Import joblib for loading the saved preprocessing + regression Pipeline
import joblib

# Import Path so the application can reliably locate model.pkl
# in the same folder as app.py
from pathlib import Path


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

# Configure the browser tab and application layout
st.set_page_config(
    page_title="E-Commerce Delivery Time Predictor",
    page_icon="📦",
    layout="centered"
)


# ---------------------------------------------------------
# LOAD THE TRAINED MODEL
# ---------------------------------------------------------

# Identify the folder in which app.py is located
BASE_DIR = Path(__file__).resolve().parent

# Create the full path to the saved model
MODEL_PATH = BASE_DIR / "model.pkl"


# Attempt to load the saved preprocessing + regression Pipeline
# If model.pkl cannot be found or loaded, the application stops
# and shows a clear error message instead of crashing silently
try:
    model = joblib.load(MODEL_PATH)

except Exception as error:

    # Display the error to the user
    st.error(
        f"The trained model could not be loaded: {error}"
    )

    # Stop the application because predictions cannot be made
    st.stop()


# ---------------------------------------------------------
# APPLICATION HEADER
# ---------------------------------------------------------

# Display the application title
st.title("📦 E-Commerce Delivery Time Predictor")


# Explain the purpose of the application
st.write(
    """
    This application uses a multiple linear regression model to estimate
    the delivery time of an e-commerce order based on order, package,
    warehouse, courier, traffic and shipping characteristics.
    """
)


# Add a visual separator
st.divider()


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

# Display a heading above the user input fields
st.subheader("Order and Delivery Information")


# Create two columns so that the application is easier to use
left_column, right_column = st.columns(2)


# ---------------------------------------------------------
# LEFT-SIDE INPUTS
# ---------------------------------------------------------

with left_column:

    # Allow the user to select one of the five valid product categories
    # These values come from the dataset specification
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


    # Allow the user to select one of the three valid shipping modes
    # These values match the categories used during model training
    shipping_mode = st.selectbox(
        "Shipping Mode",
        [
            "Standard",
            "Express",
            "Same-Day"
        ]
    )


    # Accept a positive monetary order value
    # The data dictionary states that Order_Value must be greater than zero
    order_value = st.number_input(
        "Order Value (₹)",
        min_value=0.01,
        value=6000.00,
        step=100.00
    )


    # Accept a positive package weight
    # Package weight cannot logically be zero or negative
    package_weight = st.number_input(
        "Package Weight (kg)",
        min_value=0.01,
        value=3.00,
        step=0.10
    )


    # Accept a positive warehouse-to-destination distance
    warehouse_distance = st.number_input(
        "Warehouse Distance (km)",
        min_value=0.01,
        value=400.00,
        step=10.00
    )


# ---------------------------------------------------------
# RIGHT-SIDE INPUTS
# ---------------------------------------------------------

with right_column:

    # Items_in_Order has a valid range of 1 to 10
    # Therefore the interface does not allow values outside that range
    items_in_order = st.number_input(
        "Items in Order",
        min_value=1,
        max_value=10,
        value=4,
        step=1
    )


    # Warehouse processing time must be positive
    warehouse_processing_hours = st.number_input(
        "Warehouse Processing Time (Hours)",
        min_value=0.01,
        value=3.00,
        step=0.10
    )


    # Courier_Load_Index has a valid range of 1 to 10
    courier_load_index = st.number_input(
        "Courier Load Index",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.1
    )


    # Traffic_Index also has a valid range of 1 to 10
    traffic_index = st.number_input(
        "Traffic Index",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.1
    )


# ---------------------------------------------------------
# TYPICAL-RANGE WARNINGS
# ---------------------------------------------------------

# The data dictionary states that Order_Value is typically
# between ₹300 and ₹15,000.
# These are not strict validity limits, so the application shows
# a warning rather than rejecting values outside this range.
if order_value < 300 or order_value > 15000:
    st.warning(
        "Order Value is outside the dataset's typical range of ₹300–₹15,000."
    )


# Package weight is typically between 0.1 and 15 kg
if package_weight < 0.1 or package_weight > 15:
    st.warning(
        "Package Weight is outside the dataset's typical range of 0.1–15 kg."
    )


# Warehouse distance is typically between 15 and 950 km
if warehouse_distance < 15 or warehouse_distance > 950:
    st.warning(
        "Warehouse Distance is outside the dataset's typical range of 15–950 km."
    )


# Warehouse processing time is typically between 0.5 and 6 hours
if (
    warehouse_processing_hours < 0.5
    or warehouse_processing_hours > 6
):
    st.warning(
        "Warehouse Processing Time is outside the dataset's typical range of 0.5–6 hours."
    )


# ---------------------------------------------------------
# CREATE MODEL INPUT
# ---------------------------------------------------------

# Create a single-row DataFrame using EXACTLY the same predictor names
# that were used while training the saved preprocessing Pipeline
input_data = pd.DataFrame(
    {
        "Product_Category": [product_category],
        "Shipping_Mode": [shipping_mode],
        "Order_Value": [order_value],
        "Package_Weight_Kg": [package_weight],
        "Warehouse_Distance_Km": [warehouse_distance],
        "Items_in_Order": [items_in_order],
        "Warehouse_Processing_Hours": [
            warehouse_processing_hours
        ],
        "Courier_Load_Index": [courier_load_index],
        "Traffic_Index": [traffic_index]
    }
)


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------

# Add some spacing before the prediction section
st.divider()


# Create a button so that the prediction is only generated
# when the user explicitly requests it
if st.button(
    "Predict Delivery Time",
    type="primary",
    use_container_width=True
):

    # Pass the user's inputs through the saved preprocessing
    # and multiple linear regression Pipeline
    prediction = model.predict(input_data)[0]


    # Prevent a negative prediction from being presented as a valid
    # business result because delivery time cannot logically be negative
    if prediction <= 0:

        st.error(
            "The model generated an invalid non-positive delivery-time estimate. "
            "Please review the entered values."
        )

    else:

        # Display the prediction clearly in HOURS,
        # which is the unit of the target variable
        st.metric(
            label="Predicted Delivery Time",
            value=f"{prediction:.2f} hours"
        )


        # Provide a short managerial interpretation,
        # as specifically required by the assignment
        st.info(
            f"""
            Based on the entered order and operational conditions,
            the model estimates that the order will require approximately
            **{prediction:.2f} hours** for delivery.

            A manager can use this estimate for delivery planning,
            operational coordination and customer expectation management.
            """
        )


# ---------------------------------------------------------
# MODEL INFORMATION
# ---------------------------------------------------------

# Add another separator before the explanatory section
st.divider()


# Provide a short explanation of the underlying model
with st.expander("About the Prediction Model"):

    st.write(
        """
        The prediction is generated using a Multiple Linear Regression model.

        The model uses the following predictor information:

        - Product category
        - Shipping mode
        - Order value
        - Package weight
        - Warehouse distance
        - Number of items in the order
        - Warehouse processing time
        - Courier load index
        - Traffic index

        Order_ID is not used because it is only an identifier and does not
        represent a meaningful explanatory variable.
        """
    )
