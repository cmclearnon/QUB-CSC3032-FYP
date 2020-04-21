import React, { useEffect } from 'react';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core/styles';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    '& > * + *': {
      marginTop: theme.spacing(2),
    },
  },
}));

const ErrorBanner = (props) => {
  const classes = useStyles();
  const {message} = props;
  const [error, setError] = React.useState(false);
//   const {handleClearMessage} = props;

  useEffect(() => {
    setError((message !== ''));
  });

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    props.handleClearMessage();
    // setError(false);
  };

  return (
    <div className={classes.root}>
      <Snackbar open={error} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error">
          {message}
        </Alert>
      </Snackbar>
    </div>
  );
}

export default ErrorBanner;