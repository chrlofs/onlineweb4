import React, { PropTypes } from 'react';

const OfflineIssue = ({ offlines }) => (
  <div>
    <p>Heyo</p>
  </div>
);

OfflineIssue.propTypes = {
  link: PropTypes.string.isRequired,
};

export default OfflineIssue;
