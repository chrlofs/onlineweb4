import React from 'react';
import ArticlesHeading from './ArticlesHeading';
import MainArticle from './MainArticle';
import SmallArticle from './SmallArticle';

const Articles = ({ mainArticles, smallArticles }) => (
  <div>
    <ArticlesHeading />
    <div className="row row-space">
      {
        mainArticles.map((article, index) => (
          <MainArticle article={article} key={index} />
        ))
      }
      {
        smallArticles.map((article, index) => (
          <SmallArticle article={article} key={index} />
        ))
      }
    </div>
  </div>
);

export default Articles;