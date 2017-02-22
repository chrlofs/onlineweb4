import React from 'react';
import ReactDom from 'react-dom';
import ArticlesContainer from './articles/containers/ArticlesContainer';
import EventsContainer from './events/containers/EventsContainer';
import OfflineContainer from './offline/containers/OfflineContainer';
import './initFrontpage';

ReactDom.render(
  <ArticlesContainer />,
  document.getElementById('article-items'),
);

ReactDom.render(
  <EventsContainer />,
  document.getElementById('event-items'),
);

ReactDom.render(
  <OfflineContainer />,
  document.getElementById('offline-items'),
);
