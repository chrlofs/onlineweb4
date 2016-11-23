import React, { Component } from 'react';
import Offline from '../components/Offline';


const apiOfflineToOffline = offline => ({
  offlineUrl: offline.issue,
  thumbnail: offline.get_absolute_thumbnail_url,
});


class OfflineContainer extends Component {
  constructor(props) {
    super(props);
    this.API_URL = '/api/v1/offline/?format=json';
    this.state = {
      offlines: [],
    };
    this.fetchOfflines();
  }

  fetchOfflines() {
    const apiUrl = this.API_URL;
    fetch(apiUrl, { credentials: 'same-origin' })
    .then((response) => response.json())
    .then((json) => {
      this.setState({
        offlines: json.results.map(apiOfflineToOffline),
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

export default ArticlesContainer;
