import React from 'react';
import {useState, useEffect} from 'react';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';

const columns = [
  { id: 'RegistryDate_year',
    label: 'RegistryDate_year',
    minWidth: 60,
    align: 'right'
  },
  { id: 'RegistryDate_month',
    label: 'RegistryDate_month',
    minWidth: 60,
    align: 'right'
  },
  {
    id: 'RegistryDate_day',
    label: 'RegistryDate_day',
    minWidth: 60,
    align: 'right',
    format: (value) => value.toLocaleString(),
  },
  {
    id: 'ExpirationDate_year',
    label: 'ExpirationDate_year',
    minWidth: 60,
    align: 'right',
  },
  {
    id: 'ExpirationDate_month',
    label: 'ExpirationDate_month',
    minWidth: 60,
    align: 'right',
    format: (value) => value.toLocaleString(),
  },
  {
    id: 'ExpirationDate_day',
    label: 'ExpirationDate_day',
    minWidth: 60,
    align: 'right',
    format: (value) => value.toLocaleString(),
  },
  {
    id: 'HostCountry',
    label: 'HostCountry',
    minWidth: 60,
    align: 'right',
    format: (value) => value.toLocaleString(),
  },
  {
    id: 'DomainAge',
    label: 'DomainAge',
    minWidth: 60,
    align: 'right',
    format: (value) => value.toLocaleString(),
  },
  {
    id: 'URLType',
    label: 'URLType',
    minWidth: 60,
    align: 'right',
    format: (value) => value.toLocaleString(),
  },
];

const paperclass = {
    root: {
        maxHeight: '100%',
        minHeight: '100%',
    }
}

const tableclass = {
    container: {
        maxHeight: '100%',
        minHeight: '100%',
        width: '300px'
    }
}

// const DatasetTable = (props) => {
//   const {page, total} = React.useState(0);
//   const {rowsPerPage} = React.useState(10);
//   const dataset = React.useState([]);
//   const error = React.useState(null);
//   const featureType = React.useState('host');

//   useEffect(() => {
//     fetchDataset(page);
//   })

//   handleChangePage = (event, newPage) => {
//     setPage(newPage, () => {
//       fetchDataset(page);
//     })
//     // this.setState({
//     //   page: newPage
//     // }, () => { 
//     //   this.fetchDataset(this.state.page)
//     // });
//   };

//   handleChangeRowsPerPage = (event) => {
//     set(event.target.value, () => {
//       fetchDataset(page);
//     })
//     this.setState({
//       rowsPerPage: event.target.value,
//       page: 0
//     }, () => { 
//       this.fetchDataset(this.state.page)
//     });
//   };

//   const fetchDataset = () => {
//     if (page > 0) {
//       var tmpPage = page + 1;
//     } else {
//       var tmpPage = page
//     }
//     return fetch(`http://localhost:5000/datasets?page=${tmpPage}&size=${rowsPerPage}`)
//       .then(apiResponse => apiResponse.json())
//       .then(paginatedDataset =>
//         setTotal(paginatedDataset.total),
//         setDataset(paginatedDataset.items)
//         // this.setState({
//         //   total: paginatedDataset.total,
//         //   dataset: paginatedDataset.items
//         // })
//       )
//       .catch(error =>
//         // this.setState({
//         //   error,
//         // })
//         setError(error)
//       );
//   }
// }

class DatasetTable extends React.Component {
  state = {
    page: 0,
    rowsPerPage: 10,
    dataset: [],
    total: 0,
    error: null,
  };

  componentDidMount() {
    this.fetchDataset(this.state.page)
  }

  fetchDataset = () => {
    console.log(this.props.featureType);
    const { page, rowsPerPage } = this.state
    if (page > 0) {
      var tmpPage = page + 1;
    } else {
      var tmpPage = page
    }
    return fetch(`http://localhost:5000/datasets?page=${tmpPage}&size=${rowsPerPage}`)
      .then(apiResponse => apiResponse.json())
      .then(paginatedDataset =>
        this.setState({
          total: paginatedDataset.total,
          dataset: paginatedDataset.items
        })
      )
      .catch(error =>
        this.setState({
          error,
        })
      );
  }

  handleChangePage = (event, newPage) => {
    this.setState({
      page: newPage
    }, () => { 
      this.fetchDataset(this.state.page)
    });
  };

  handleChangeRowsPerPage = (event) => {
    this.setState({
      rowsPerPage: event.target.value,
      page: 0
    }, () => { 
      this.fetchDataset(this.state.page)
    });
  };

  render() {
    const {page, rowsPerPage, total} = this.state
    const {dataset} = this.state
    return (
      <Paper className={paperclass.root} elevation={3}>
      <TableContainer className={tableclass.container}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
        </Table>
        <div style={{ overflow: 'auto', height: '550px'}}>
          <Table style={{tableLayout: 'fixed'}}>  
            <TableBody>
                {dataset.slice(0, rowsPerPage).map((row, index) => {
                return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                    {columns.map((column, colIndex) => {
                        const value = row[column.id];
                        return (
                        <TableCell key={index+colIndex} align={column.align}>
                            {column.format && typeof value === 'number' ? column.format(value) : value}
                        </TableCell>
                        );
                    })}
                    </TableRow>
                );
                })}
            </TableBody>
          </Table>
        </div>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={total}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={this.handleChangePage}
        onChangeRowsPerPage={this.handleChangeRowsPerPage}
      />
    </Paper>
    )
  };
}

export default DatasetTable;