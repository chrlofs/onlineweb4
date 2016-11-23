import React, { PropTypes } from 'react';
import Heading from 'common/Heading';

const Offline = ({ offlines }) => (
  <div>
    <Heading name={"OFFLINE"}/>
    <div className="row row-space">
      {
        mainArticles.map((article, index) => (
          <MainArticle {...article} key={index} />
        ))
      }
      {
        smallArticles.map((article, index) => (
          <SmallArticle {...article} key={index} />
        ))
      }
    </div>
  </div>
);

Articles.propTypes = {
  mainArticles: PropTypes.arrayOf(PropTypes.shape(MainArticle.propTypes)),
  smallArticles: PropTypes.arrayOf(PropTypes.shape(SmallArticle.propTypes)),
};


export default Articles;
