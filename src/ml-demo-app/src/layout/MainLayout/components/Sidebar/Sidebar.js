import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import StorageIcon from '@material-ui/icons/Storage';
import { Link } from 'react-router-dom';

const drawerWidth = 240;

const useStyles = makeStyles(() => ({
  root: {
    display: 'flex',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerContainer: {
    overflow: 'auto',
  },
}));

function ListItemLink(props) {
  const {primary, to, icon} = props;

  const renderLink = React.useMemo(
    () => React.forwardRef((itemProps, ref) => <Link to={to} ref={ref} {...itemProps} />),
    [to],
  );

  return (
    <li>
      <ListItem button component={renderLink} key={primary}>
        {icon ? <ListItemIcon>{icon}</ListItemIcon> : null}
        <ListItemText primary = {primary} />
      </ListItem>
    </li>
  )
}

ListItemLink.propTypes = {
  icon: PropTypes.element,
  primary: PropTypes.string.isRequired,
  to: PropTypes.string.isRequired,
};

const Sidebar = () => {
  const classes = useStyles();

  const pages = [
    {
      title: 'Model Dashboard',
      href: '/dashboard',
      icon: <DashboardIcon />
    },
    {
      title: 'Datasets',
      href: '/datasets',
      icon: <StorageIcon />
    }
  ];

  return (
    <div className={classes.root}>
      <Drawer
        className={classes.drawer}
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <Toolbar />
        <div className={classes.drawerContainer}>
          <List>
            {pages.map((item, index) => (
              <ListItemLink to={item.href} primary={item.title} key={item.title}/>
            ))}
          </List>
          <Divider />
        </div>
      </Drawer>
    </div>
  );
}

export default Sidebar;