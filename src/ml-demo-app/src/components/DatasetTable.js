import React from 'react';
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

const DatasetTable = (props) => {
  const rows = props.items;
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

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
                {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => {
                return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                    {columns.map((column) => {
                        const value = row[column.id];
                        return (
                        <TableCell key={column.id} align={column.align}>
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
        count={rows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
    </Paper>
  );
}

export default DatasetTable;