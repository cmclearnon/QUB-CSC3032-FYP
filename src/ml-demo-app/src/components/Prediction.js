import React from 'react';
import Pred from './Pred';

function PredProba(props){
return <p> {props.predProba}</p>
}

class Prediction extends React.Component {
    render() {
        const p = this.props;
        return (
            <div className="prediction">
            <p style={{ color: 'red' }}> {p.predProba}</p>
            </div>
        );
    }
  }

  export default Prediction;
  