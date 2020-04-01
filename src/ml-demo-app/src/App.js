import React, { useState, useEffect } from 'react';
import URLForm from './components/URLForm';
import Prediction from './components/Prediction';
import { Box, Heading, Button, Grommet, Collapsible, Layer, ResponsiveContext, Grid } from 'grommet';
import { TextInput } from 'grommet';
import { Menu, FormClose } from 'grommet-icons';

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '20px',
      height: '22px',
    },
  },
};

const AppBar = (props) => (
  <Box
    tag='header'
    direction='row'
    align='center'
    justify='between'
    background='black'
    pad={{ left: 'medium', right: 'small', vertical: 'small' }}
    elevation='medium'
    style={{ zIndex: '1' }}
    {...props}
  />
);

class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {
        url: '',
        pred_proba: [],
        showSidebar: false,
    };
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
    const { showSidebar } = this.state;
    return (
      // <div className="App">
      <Grommet theme={theme} full>
              <ResponsiveContext.Consumer>
          {size => (
            <Box fill>
              <AppBar>
                <Button
                  icon={<Menu />}
                  onClick={() => this.setState({ showSidebar: !this.state.showSidebar })}
                />
                <Heading level='3' margin='none'>Malicious URL Detection w/ML</Heading>
                {/* <Button
                  icon={<Menu />}
                  onClick={() => this.setState({ showSidebar: !this.state.showSidebar })}
                /> */}
              </AppBar>
              <Box direction='row' flex overflow={{ horizontal: 'hidden' }}>
                <Box flex align='left' justify='centre' background='light-5'>
                  <Grid
                    rows={['xxsmall', 'medium']}
                    columns={['medium', 'medium']}
                    gap="small"
                    areas={[
                      { name: 'header', start: [0, 0], end: [1, 0] },
                      { name: 'nav', start: [0, 1], end: [0, 1] },
                      { name: 'main', start: [1, 1], end: [1, 1] },
                    ]}
                  >
                    <Box gridArea="header" background="teal" />
                    <Box gridArea="nav" background="white">
                      <form onSubmit={this.handleSubmit}>
                          {/* <input name="url" type="text" placeholder="URL" value={this.state.url} onChange={this.handleURLChange}/> */}
                          <TextInput
                            placeholder="URL"
                            value={this.state.url}
                            onChange={this.handleURLChange}
                          />
                          {/* <button>Predict</button> */}
                          <Button label='Submit' onClick={this.handleSubmit} />
                          <Prediction predProba = {this.state.pred_proba}/>
                      </form>
                    </Box>
                    <Box gridArea="main" background="white" />
                  </Grid>
                </Box>
                {(!showSidebar || size !== 'small') ? (
                  <Collapsible direction="horizontal" open={showSidebar}>
                    <Box
                      flex
                      width='medium'
                      background='light-2'
                      elevation='small'
                      align='center'
                      justify='center'
                    >
                      sidebar
                    </Box>
                  </Collapsible>
                ): (
                  <Layer>
                    <Box
                      background='light-2'
                      tag='header'
                      justify='end'
                      align='center'
                      direction='row'
                    >
                      {/* <Button
                        icon={<FormClose />}
                        onClick={() => this.setState({ showSidebar: false })}
                      /> */}
                    </Box>
                  </Layer>
                )}
              </Box>
            </Box>
          )}
        </ResponsiveContext.Consumer>
      </Grommet>
    );
  }
}

export default App;
