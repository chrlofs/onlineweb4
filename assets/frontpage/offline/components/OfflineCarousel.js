import React, { PropTypes } from 'react';
import OfflineIssue from './OfflineIssue';

class OfflineCarousel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      carouselPageIndex: 0,
      offlinesToRender: [],
    };
    this.setOfflinesToRender();
  }

  setOfflinesToRender() {
    if (!this.props.offlines || !this.props.offlines.length) {
      return;
    }
    this.setState({
      offlinesToRender: this.props.offlines.slice(this.state.carouselPageIndex, this.state.carouselPageIndex + 3),
    });
  }

  button(right) {
    let mod = 1;
    mod = right ? 1 : -1;
    if (!right && this.carouselPageIndex + (3 * mod) < 0) {
      this.setState({
        carouselPageIndex: Math.floor((this.offlines.lenght / 3)),
      });
    }
    else if (this.carouselPageIndex + (3 * mod) > Math.floor((this.offlines.length / 3)) ||
        this.carouselPageIndex + (3 * mod) < 0) {
      this.setState({
        carouselPageIndex: 0,
      });
    } else {
      this.setState({
        carouselPageIndex: this.carouselPageIndex + (3 * mod),
      });
    }
  }

  render() {
    return (
      <div>
        <button type="button" onClick={() => this.button(true)} />
        <OfflineIssue offlines={this.offlines} />
        <button type="button" onClick={() => this.button(false)} />
      </div>
    );
  }
}

OfflineCarousel.propTypes = {
  offlines: PropTypes.arrayOf(PropTypes.shape(OfflineIssue.propTypes)),
};

export default OfflineCarousel;
