import React from 'react';
import ReactDom from 'react-dom';
import OfflineContainer from './containers/OfflineContainer'

require('es6-promise').polyfill();
require('isomorphic-fetch');

ReactDom.render(
  <OfflineContainer />,
  document.getElementById('offline-items'),
);
