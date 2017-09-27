import React from 'react';
import ReactDom from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import MeetApp from './containers/meetapp';
import './less/meetapp.less';

console.log("running");
const renderMeetapp = () => {
    ReactDom.render(
        <AppContainer>
            <MeetApp/>
        </AppContainer>,
        document.getElementById('meetapp'),
    );
};

renderMeetapp();

if (module.hot) {
    module.hot.accept('./containers/meetapp', () => {
        renderMeetapp();
    });
}
