import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import {Sidebar} from './components/Sidebar';
import PropTypes from 'prop-types';
import clsx from 'clsx';

const useStyles = makeStyles((theme) => ({
  root: {
    paddingTop: 15,
    height: '100%',
  },
  shiftContent: {
    paddingLeft: 180
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    color: theme.palette.secondary.main
  },
  heading: {
    color: 'secondary'
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(8),
    height: '100%'
  },
}));

export default function MainLayout(props) {
  const classes = useStyles();
  const { children } = props;

  return (
    <div className={clsx({
        [classes.root]: true,
        [classes.shiftContent]: true
      })}
    >
      <CssBaseline />
      <AppBar position="fixed" className={classes.appBar} color={classes.appBar.color}>
        <Toolbar>
          <Typography variant="h6" noWrap className={classes.heading}>
            Malicious URL Detection
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar/>
      <main className={classes.content}>
        {children}
      </main>
    </div>
  );
}

MainLayout.propTypes = {
  children: PropTypes.node
};