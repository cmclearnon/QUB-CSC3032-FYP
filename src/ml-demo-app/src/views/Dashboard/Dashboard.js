import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';
import { ModelAccuracy } from './components/ModelAccuracy';
import { PredictionsMetrics } from './components/PredictionMetrics';
import { SingleClassification } from './components/SingleClassification';
import { Features } from './components/FeatureExtraction';
import { URLInput } from './components/URLInput';
import { ErrorBanner } from './components/ErrorBanner';

// const useStyles = makeStyles(theme => ({
//     root: {
//       padding: theme.spacing(4)
//     },
//     content: {
//         flexGrow: 1,
//     }
// }));


class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          url: "",
          model: "",
          prediction: -1,
          probabilityList: [0, 0],
          metrics: [],
          error: false,
          message: "",
          accuracy: null,
          tpr: null,
          fnr: null,
          auc_score: null,
          features: []
        }
        this.getPrediction = this.getPrediction.bind(this);
        this.handleClearMessage = this.handleClearMessage.bind(this);
    }
// const Dashboard = () => {
    // classes = useStyles()
    classes = makeStyles(theme => ({
        root: {
          padding: theme.spacing(4)
        },
        content: {
            flexGrow: 1,
        },
        errorMessage: {
          backgroundcolor: theme.palette.error.main,
          color: theme.palette.error.contrastText,
          padding: theme.padding('1em')
        }
    }));

    componentDidMount() {
        this.getMetrics()
    }

    handleClearMessage = () => {
      this.setState({
        message: ''
      })
    }

    getPrediction = (url, model, feature) => {
      console.log(`http://localhost:5000/single_prediction?model=${model}&featureType=${feature}&url=${url}`)
        return fetch(`http://localhost:5000/single_prediction?model=${model}&featureType=${feature}&url=${url}`)
          .then(apiResponse => apiResponse.json())
          .then(predictionResults =>
            this.setState({
              url: url,
              prediction: predictionResults.prediction,
              probabilityList: predictionResults.probability[0],
              features: predictionResults.original_features,
              error: predictionResults.error,
            }),
          )
          .catch(error =>
            this.setState({
              error,
              error: true,
              message: 'Oops! Looks like a problem occured predicting that URL'
            })
          );
    }

    getMetrics = () => {
        return fetch(`http://localhost:5000/model_accuracy`)
          .then(apiResponse => apiResponse.json())
          .then(metricsResults =>
            this.setState({
              accuracy: metricsResults.accuracy,
              tpr: metricsResults.tpr,
              fnr: metricsResults.fnr,
              auc_score: metricsResults.auc_score,
            })
          )
          .catch(error =>
            this.setState({
              error,
              error: true,
              message: 'Oops! Looks like a problem occured retrieving model metrics'
            })
          );
    }

    render() {
        return (
            <div className = {this.classes.root}>
              {/* {this.state.error && <div className="error-message">{this.state.message}</div>} */}
              <Grid className = {this.classes.content} container spacing={8}>
                    <Grid item lg = {4} sm = {6} xs = {12} zl = {3}>
                        <URLInput getPrediction={this.getPrediction}/>
                    </Grid>
                </Grid>
                <Grid className = {this.classes.content} container spacing={8}>
                    {/* <Grid item lg = {4} sm = {6} xs = {12} zl = {3}>
                        <URLInput getPrediction={this.getPrediction}/>
                    </Grid> */}
                    <Grid item lg = {3} sm = {6} xs = {12} zl = {3}>
                        <ModelAccuracy accuracy={this.state.accuracy} auc_score={this.state.auc_score}/>
                    </Grid>
                    <Grid item lg = {4} sm = {6} xs = {12} zl = {3}>
                        <SingleClassification probabilityList={this.state.probabilityList} classification={this.state.prediction}/>
                    </Grid>
                </Grid>
                <Grid className = {this.classes.content} container spacing={10}>
                    <Grid item lg={4} md={6} xl={3} xs={12}>
                        <PredictionsMetrics tpr={this.state.tpr} fnr={this.state.fnr}/>
                    </Grid>
                    <Grid item lg={5} md={6} xl={3} xs={12}>
                        <Features url={this.state.url} features={{...this.state.features[0]}}/>
                    </Grid>
                </Grid>
                <ErrorBanner message={this.state.message} handleClearMessage={this.handleClearMessage}/>
            </div>
        );
    };
};
export default Dashboard;