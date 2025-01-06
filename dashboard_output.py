import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class HydraulicNetworkAnalysis:
    def __init__(self):
        self.nodes = {}
        self.conduits = {}
        self.surge_tank = {}
        self.orifice = {}
        self.reservoir = {}
        self.flow_schedule = {}
        self.computational_params = {}

    def add_node(self, node_number, elevation):
        """Add a node to the network"""
        self.nodes[node_number] = elevation

    def add_conduit(self, conduit_id, length, diameter, thickness, manning, material, celerity, cplus, cminus, numseg):
        """Add a conduit to the network"""
        self.conduits[conduit_id] = {
            'length': length,
            'diameter': diameter,
            'thickness': thickness,
            'manning': manning,
            'material': material,
            'celerity': celerity,
            'cplus': cplus,
            'cminus': cminus,
            'numseg': numseg
        }

    def set_surge_tank(self, diameter, top_elevation, bottom_elevation, material, thickness, manning, celerity):
        """Set surge tank properties"""
        self.surge_tank = {
            'diameter': diameter,
            'top_elevation': top_elevation,
            'bottom_elevation': bottom_elevation,
            'material': material,
            'thickness': thickness,
            'manning': manning,
            'celerity': celerity
        }

    def set_orifice(self, diameter, cd_upward, cd_downward, cplus, cminus):
        """Set orifice properties"""
        self.orifice = {
            'diameter': diameter,
            'cd_upward': cd_upward,
            'cd_downward': cd_downward,
            'cplus': cplus,
            'cminus': cminus
        }

    def set_reservoir(self, water_level):
        """Set reservoir water level"""
        self.reservoir = {'water_level': water_level}

    def add_flow_schedule(self, time_points, discharge_points):
        """Add flow schedule"""
        self.flow_schedule = {
            'time': time_points,
            'discharge': discharge_points
        }

    def set_computational_params(self, dtcomp, dtout, tmax):
        """Set computational parameters"""
        self.computational_params = {
            'dtcomp': dtcomp,
            'dtout': dtout,
            'tmax': tmax
        }

    def visualize_network(self):
        """Create a visualization of the hydraulic network"""
        if not self.nodes:
            st.warning("No nodes defined. Please add nodes first.")
            return None

        plt.figure(figsize=(12, 6))
        
        # Plot nodes
        for node, elevation in self.nodes.items():
            plt.scatter(node, elevation, c='blue', s=100)
            plt.text(node, elevation, f'Node {node}\n{elevation}m', 
                     verticalalignment='bottom', horizontalalignment='center')
        
        plt.title('Hydraulic Network Node Elevations')
        plt.xlabel('Node Number')
        plt.ylabel('Elevation (m)')
        plt.tight_layout()
        return plt

    def analyze_network(self, inputs):
        """Perform network analysis and return results"""
        results = {}
        for input_item in inputs:
            if input_item.startswith("NODE"):
                node_number = int(input_item.split()[1])
                results[node_number] = {
                    "Q": 100,  # Example data
                    "HEAD": 50,  # Example data
                    "PRESSURE": 300  # Example data
                }
            elif input_item.startswith("ELEM"):
                elem_id = input_item.split()[1]
                results[elem_id] = {
                    "Q": 200,  # Example data
                    "ELEV": 30  # Example data
                }
        return results

def main():
    st.set_page_config(page_title="Hydraulic Network Analysis", layout="wide")
    
    analysis = HydraulicNetworkAnalysis()

    # Sidebar for CSV upload or manual input
    st.sidebar.title("Input Options")
    input_mode = st.sidebar.radio("Choose Input Method:", ["Upload CSV", "Manual Input"])

    if input_mode == "Upload CSV":
        st.header("Upload CSV File")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.subheader("Uploaded Data")
            st.dataframe(data)

    elif input_mode == "Manual Input":
        # Simplified Navigation for Manual Input
        menu = st.sidebar.radio("Navigation", [
            "Nodes", "Conduits", "Surge Tank", 
            "Orifice", "Reservoir", "Flow Schedule", 
            "Computational Parameters", "Network Analysis"
        ])

        # Nodes Input
        if menu == "Nodes":
            st.header("Node Input")
            with st.form("node_input"):
                node_number = st.number_input("Node Number", min_value=1, step=1)
                elevation = st.number_input("Elevation (m)", min_value=0.0, step=0.1)
                submit = st.form_submit_button("Add Node")
                
                if submit:
                    analysis.add_node(node_number, elevation)
                    st.success(f"Node {node_number} added with elevation {elevation}m")
            
            # Display current nodes
            if analysis.nodes:
                st.subheader("Current Nodes")
                nodes_df = pd.DataFrame.from_dict(analysis.nodes, orient='index', columns=['Elevation (m)'])
                nodes_df.index.name = 'Node Number'
                st.dataframe(nodes_df)

        # Conduits Input
        elif menu == "Conduits":
            st.header("Conduit Input")
            with st.form("conduit_input"):
                conduit_id = st.text_input("Conduit ID")
                length = st.number_input("Length (m)", min_value=0.0, step=0.1)
                diameter = st.number_input("Diameter (m)", min_value=0.0, step=0.1)
                thickness = st.number_input("Thickness (m)", min_value=0.0, step=0.001)
                manning = st.number_input("Manning's Coefficient", min_value=0.0, step=0.001)
                material = st.selectbox("Material", ["Concrete", "Steel"])
                celerity = st.number_input("Celerity (m/s)", min_value=0.0, step=1.0)
                cplus = st.number_input("CPLUS", min_value=0.0, step=0.01)
                cminus = st.number_input("CMINUS", min_value=0.0, step=0.01)
                numseg = st.number_input("NUMSEG", min_value=1, step=1)
                submit = st.form_submit_button("Add Conduit")
                
                if submit:
                    analysis.add_conduit(conduit_id, length, diameter, thickness, 
                                         manning, material, celerity, 
                                         cplus, cminus, numseg)
                    st.success(f"Conduit {conduit_id} added")
            
            # Display current conduits
            if analysis.conduits:
                st.subheader("Current Conduits")
                conduits_df = pd.DataFrame.from_dict(analysis.conduits, orient='index')
                st.dataframe(conduits_df)

        # Additional sections for Surge Tank, Orifice, Reservoir, Flow Schedule, and Computational Parameters
        elif menu == "Surge Tank":
            st.header("Surge Tank Input")
            # Implementation here

        elif menu == "Orifice":
            st.header("Orifice Input")
            # Implementation here

        elif menu == "Reservoir":
            st.header("Reservoir Input")
            # Implementation here

        elif menu == "Flow Schedule":
            st.header("Flow Schedule Input")
            # Implementation here

        elif menu == "Computational Parameters":
            st.header("Computational Parameters")
            with st.form("comp_params_input"):
                dtcomp = st.number_input("DTCOMP", value=0.01, min_value=0.0, step=0.01)
                dtout = st.number_input("DTOUT", value=0.1, min_value=0.0, step=0.1)
                tmax = st.number_input("TMAX", value=500.0, min_value=0.0, step=1.0)
                submit = st.form_submit_button("Set Parameters")
                
                if submit:
                    analysis.set_computational_params(dtcomp, dtout, tmax)
                    st.success("Computational parameters set")
            
            # Display computational parameters
            if analysis.computational_params:
                st.subheader("Computational Parameters")
                params_df = pd.DataFrame.from_dict(analysis.computational_params, orient='index', columns=['Value'])
                st.dataframe(params_df)

        # Network Analysis
        elif menu == "Network Analysis":
            st.header("Network Analysis")
        
        # Network Visualization
        st.subheader("Network Visualization")
        plt_fig = analysis.visualize_network()
        if plt_fig:
            st.pyplot(plt_fig)

    # Network Analysis and Output
    st.header("Network Analysis and Output")
    with st.form("network_analysis_output"):
        inputs = st.text_area("Inputs (e.g., NODE 10\nELEM ST\nNODE 3)").splitlines()
        submit = st.form_submit_button("Analyze")
        
        if submit:
            results = analysis.analyze_network(inputs)
            st.subheader("Analysis Result")
            st.write(results)

            # Print the results in the specified format
            for input_item in inputs:
                if input_item.startswith("NODE"):
                    st.write(f"{input_item}: Q HEAD PRESSURE")
                elif input_item.startswith("ELEM"):
                    st.write(f"{input_item}: Q ELEV")

            # Plot the results
            if results:
                for key, value in results.items():
                    for output, result in value.items():
                        plt.figure(figsize=(10, 5))
                        plt.plot([key], [result], marker='o', label=f'{output}')
                        plt.title('Analysis Results')
                        plt.xlabel('Node/Element')
                        plt.ylabel(output)
                        plt.legend()
                        plt.grid(True)
                        st.pyplot(plt)

if __name__ == "__main__":
    main()
