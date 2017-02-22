import React, { PropTypes } from 'react';
import OfflineBlurb from './OfflineBlurb';
import OfflineCarousel from './OfflineCarousel';
import Heading from '../../common/Heading'

const Offline = ({ offlines }) => (
  <div>
    <Heading />
    <div className="row">
      {
        <OfflineBlurb
          ingress="Offline er Online sitt eget tidsskrift og så dagens lys i mars 2011. Profil- og aviskomiteen står for det grafiske og redaksjonelle ansvaret, og har i tillegg eksterne skribenter i andre deler av Online."
          p1="Offline gis ut to ganger i semesteret og inneholder en fin blanding av underholdende og opplysende saker myntet på informatikkstudenter."
          p2="Ønsker du å abonnere på magasinet og få tilsendt papirutgaven i posten kan du gå inn å registrere deg gjennom vårt googleskjema: "
          p3="Ellers finner du alle utgavene i PDF-format til høyre. God lesing!"
          orderLinkText="Bestillingsskjema"
          orderLink="http://goo.gl/wksFS"
        />
      }
    </div>
    <OfflineCarousel offlines={offlines} />
  </div>
);

Offline.propTypes = {
  offlines: OfflineCarousel.propTypes.offlines,
};


export default Offline;
