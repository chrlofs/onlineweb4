import React, {PropTypes} from 'react';

const OfflineBlurb = ({ingress, p1, p2, p3, orderLinkText, orderLink}) => (
  <div>
    <div className="ingress">
      <p>{ ingress }</p>
    </div>
    <p>{ p1 }</p>
    <p>{ p2 }<a href="{ orderLinkText }">{ orderLink }</a></p>
    <p>{ p3 }</p>
  </div>
);

OfflineBlurb.propTypes = {
  ingress: PropTypes.string.isRequired,
  p1: PropTypes.string.isRequired,
  p2: PropTypes.string.isRequired,
  p3: PropTypes.string.isRequired,
  orderLinkText: PropTypes.string.isRequired,
  orderLink: PropTypes.string.isRequired,
};

export default OfflineBlurb;
