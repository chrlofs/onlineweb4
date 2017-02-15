import React, { PropTypes } from 'react';
import Offline from '../components/Offline';

const apiOfflinesToOfflines = offline => ({
  offlineUrl: offline.issue,
  thumb: `${offline.issue}.thumb.png`,
});

class OfflineContainer extends React.Component {
  constructor(props) {
    super(props);
    this.API_URL = '/api/v1/articles?format=json';
    this.state = {
      offlines: [],
    };
    this.fetchOfflines();
  }

  fetchOfflines() {
    const apiURL = this.API_URL;
    fetch(apiURL, { credentials: 'same-origin' })
    .then(response => response.json())
    .then((json) => {
      this.setState({
        offlines: json.results.map(apiOfflinesToOfflines),
      });
    });
  }

  render() {
    return (
      <Offline
        offlines={this.offlines}
      />
    );
  }
}

export default OfflineContainer;
