import React, { useState, useEffect } from 'react';
import URLForm from './components/URLForm';
import DatasetTable from './components/DatasetTable';
import Prediction from './components/Prediction';
import { Box, Heading, Header, Anchor, Footer, Title, Menu, Button, Grommet, ResponsiveContext, Grid, Sidebar } from 'grommet';
import { Text } from 'grommet';

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '20px',
      height: '22px',
    },
  },
};

class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {
        url: '',
        pred_proba: [],
        page: 1,
        rowsPerPage: 100,
        total: 0,
        dataset: [],
        error: null
    };
  }

  fetchDataset = () => {
    const { page, rowsPerPage } = this.state
    return fetch(`http://localhost:5000/datasets?page=${page}&size=${rowsPerPage}`)
      .then(apiResponse => apiResponse.json())
      .then(paginatedDataset =>
        this.setState({
          page: paginatedDataset.page,
          total: paginatedDataset.total,
          dataset: paginatedDataset.items
        })
      )
      .catch(error =>
        this.setState({
          error
        })
      );
  }


  componentDidMount() {
    this.fetchDataset()
    console.log(this.state.total)
  }

  handleSubmit(event) {
    event.preventDefault();
    const urlToPredict = this.state.url;
    console.log(urlToPredict)
    
    var apiRequestURL = `/predict?url=${urlToPredict}`
    let currentComponent = this;
    fetch(apiRequestURL).then((res) => res.json()).then(function(data) {
        const responseJSON = data;
        currentComponent.setState({
          pred_proba: responseJSON.predict_proba[0][1]
        });
        console.log(currentComponent.state.pred_proba);
    })
  }
  
  handleURLChange = (event) => {
      this.setState({url: event.target.value});
  }

  render() {
    return (
      <Grommet full theme={theme}>
      <Grid
        fill
        rows={["auto", "flex"]}
        columns={["auto", "flex"]}
        areas={[
          { name: "header", start: [0, 0], end: [1, 0] },
          { name: "sidebar", start: [0, 1], end: [0, 1] },
          { name: "main", start: [1, 1], end: [1, 1] }
        ]}
      >
        <Box
          gridArea="header"
          direction="row"
          align="center"
          justify="between"
          pad={{ horizontal: "medium", vertical: "small" }}
          background="dark-1"
        >
          <Text size="large">Malicious URL Detection</Text>
        </Box>
          <Box
            gridArea="sidebar"
            background="dark-2"
            width="small"
            animation={[
              { type: "fadeIn", duration: 300 },
              { type: "slideRight", size: "xlarge", duration: 150 }
            ]}
          >
            {["Dashboard", "Datasets", "Transformations"].map(name => (
              <Button key={name} href="#" hoverIndicator>
                <Box pad={{ horizontal: "medium", vertical: "small" }}>
                  <Text>{name}</Text>
                </Box>
              </Button>
            ))}
          </Box>
        <Box 
          gridArea="main"
          justify="center"
          align="center"
          pad={{ horizontal: "medium", vertical: "small" }}
        >
          <DatasetTable items={this.state.dataset} page={this.state.page} rowsPerPage={this.state.rowsPerPage}/>
        </Box>
      </Grid>
    </Grommet>
      // <Grommet theme={theme} full>
      //         <ResponsiveContext.Consumer>
      //     {size => (
      //       <Box fill>
      //         <AppBar>
      //           <Heading level='3' margin='none'>Malicious URL Detection w/ML</Heading>
      //         </AppBar>
      //         <Box direction='row' flex overflow={{ horizontal: 'hidden' }}>
      //           <Box flex align='left' justify='centre' background='light-5'>
      //             <Grid
      //               rows={['xxsmall', 'medium']}
      //               columns={['medium', 'medium']}
      //               gap="small"
      //               areas={[
      //                 { name: 'header', start: [0, 0], end: [1, 0] },
      //                 { name: 'nav', start: [0, 1], end: [0, 1] },
      //                 { name: 'main', start: [1, 1], end: [1, 1] },
      //               ]}
      //             >
      //               <Box gridArea="header" background="teal" />
      //               <Box gridArea="nav" background="white">
      //                 <form onSubmit={this.handleSubmit}>
      //                     {/* <input name="url" type="text" placeholder="URL" value={this.state.url} onChange={this.handleURLChange}/> */}
      //                     <TextInput
      //                       placeholder="URL"
      //                       value={this.state.url}
      //                       onChange={this.handleURLChange}
      //                     />
      //                     {/* <button>Predict</button> */}
      //                     <Button label='Submit' onClick={this.handleSubmit} />
      //                     <Prediction predProba = {this.state.pred_proba}/>
      //                 </form>
      //               </Box>
      //               <Box gridArea="main" background="white" />
      //             </Grid>
      //           </Box>
      //         </Box>
      //       </Box>
      //     )}
      //   </ResponsiveContext.Consumer>
      // </Grommet>
    );
  }
}

export default App;
