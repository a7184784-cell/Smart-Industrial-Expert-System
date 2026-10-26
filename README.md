# 🏭 Smart Industrial Expert System

An advanced desktop-based Industrial Expert System built with Python, Pandas, and Tkinter[cite: 10]. This application performs automated fault diagnosis, risk assessment, and decision support for industrial machinery using real-world sensor datasets (`AI4I 2020`)[cite: 10].

## 🚀 Key Features

* **Graphical User Interface (GUI):** An intuitive, interactive dark-themed desktop dashboard built using `Tkinter`[cite: 10].
* **Rule-Based Inference Engine:** Implements precise `IF-THEN` logical rules to evaluate machine operational parameters and detect critical industrial failures[cite: 10].
* **Automated Fault Detection:** Identifies multiple failure modes including:
  * **TWF:** Tool Wear Failure[cite: 10]
  * **HDF:** Heat Dissipation Failure[cite: 10]
  * **PWF:** Power Failure[cite: 10]
  * **OSF:** Overstrain Failure[cite: 10]
  * **RNF:** Random Failure[cite: 10]
* **Dynamic Data Visualization:** Integrated `Matplotlib` dashboard providing real-time visual charts of sensor metrics (Air Temperature, Process Temperature, Rotational Speed, Torque, and Tool Wear) alongside machine status indicators[cite: 10].
* **Flexible Analysis Modes:** Allows users to analyze random machine samples or query specific machinery data via unique Identification numbers (`ID`)[cite: 10].
* **System Statistics:** Comprehensive statistical pop-up window tracking overall machine health rates, failure distributions, and operational percentages[cite: 10].

## 🛠️ Technologies & Libraries

* **Python 3.x**[cite: 10]
* **Pandas:** For data manipulation and reading CSV sensor logs[cite: 10]
* **Matplotlib:** For rendering analytical graphical charts[cite: 10]
* **Tkinter / ttk:** For desktop GUI architecture and widgets[cite: 10]

## 📂 Project Structure

```text
Smart-Industrial-Expert-System/
│
├── uo.py                # Main application script & GUI controller
├── ai4i2020.csv         # Industrial sensor dataset
├── requirements.txt     # Required Python packages
└── README.md            # Project documentation