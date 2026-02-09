export const vastXml = `<VAST version="4.2" xmlns="http://www.iab.com/VAST">
  <Ad id="dt-842e3cf0f0d6">
    <InLine>
      <AdSystem>DreamTraffic</AdSystem>
      <AdTitle>DreamTraffic Hero - Luma AI Dream Machine</AdTitle>
      <Advertiser>Luma AI</Advertiser>
      <Impression id="dt-imp">
        https://track.dreamtraffic.demo/impression?id=dt-842e3cf0f0d6&amp;cb=[CACHEBUSTING]
      </Impression>
      <AdVerifications>
        <Verification vendor="ias-pub-291582">
          <JavaScriptResource apiFramework="omid" browserOptional="true">
            https://fw.adsafeprotected.com/rfw/dv/fwjsvid/st/291582/36966574.js
          </JavaScriptResource>
          <TrackingEvents>
            <Tracking event="verificationNotExecuted">
              https://pixel.adsafeprotected.com/services/pub/verify-not-executed?vendor=ias
            </Tracking>
          </TrackingEvents>
          <VerificationParameters>
            {"partner":"com.ias","vendorKey":"ias-pub-291582"}
          </VerificationParameters>
        </Verification>
        <Verification vendor="moat-dreamtraffic">
          <JavaScriptResource apiFramework="omid" browserOptional="true">
            https://z.moatads.com/dreamtrafficpixel/moatvideo.js
          </JavaScriptResource>
          <TrackingEvents>
            <Tracking event="verificationNotExecuted">
              https://z.moatads.com/dreamtrafficpixel/verify-not-executed?vendor=moat
            </Tracking>
          </TrackingEvents>
          <VerificationParameters>
            {"partner":"com.moat","vendorKey":"moat-dreamtraffic"}
          </VerificationParameters>
        </Verification>
        <Verification vendor="dv-ctx-123456">
          <JavaScriptResource apiFramework="omid" browserOptional="true">
            https://cdn.doubleverify.com/dvbs_src.js
          </JavaScriptResource>
          <TrackingEvents>
            <Tracking event="verificationNotExecuted">
              https://cdn.doubleverify.com/dvbs_src.js/verify-not-executed?vendor=doubleverify
            </Tracking>
          </TrackingEvents>
          <VerificationParameters>
            {"partner":"com.doubleverify","vendorKey":"dv-ctx-123456"}
          </VerificationParameters>
        </Verification>
      </AdVerifications>
      <Creatives>
        <Creative id="creative-dt-842e3cf0f0d6" adId="dt-842e3cf0f0d6">
          <Linear>
            <Duration>00:00:06</Duration>
            <MediaFiles>
              <MediaFile delivery="progressive" type="video/mp4"
                         width="720" height="1280" codec="H.264" bitrate="3700">
                https://dreamtraffic-demo.vercel.app/dreamtraffic-hero-6s.mp4
              </MediaFile>
            </MediaFiles>
            <TrackingEvents>
              <Tracking event="start">
                https://track.dreamtraffic.demo/start?id=dt-842e3cf0f0d6
              </Tracking>
              <Tracking event="firstQuartile">
                https://track.dreamtraffic.demo/firstQuartile?id=dt-842e3cf0f0d6
              </Tracking>
              <Tracking event="midpoint">
                https://track.dreamtraffic.demo/midpoint?id=dt-842e3cf0f0d6
              </Tracking>
              <Tracking event="thirdQuartile">
                https://track.dreamtraffic.demo/thirdQuartile?id=dt-842e3cf0f0d6
              </Tracking>
              <Tracking event="complete">
                https://track.dreamtraffic.demo/complete?id=dt-842e3cf0f0d6
              </Tracking>
              <Tracking event="pause">
                https://track.dreamtraffic.demo/pause?id=dt-842e3cf0f0d6
              </Tracking>
              <Tracking event="resume">
                https://track.dreamtraffic.demo/resume?id=dt-842e3cf0f0d6
              </Tracking>
            </TrackingEvents>
            <VideoClicks>
              <ClickThrough id="dt-click">https://lumalabs.ai</ClickThrough>
              <ClickTracking id="dt-click-track">
                https://track.dreamtraffic.demo/click?id=dt-842e3cf0f0d6
              </ClickTracking>
            </VideoClicks>
          </Linear>
        </Creative>
      </Creatives>
    </InLine>
  </Ad>
</VAST>`

export const trackingEvents = [
  { event: 'impression', description: 'Ad loaded in player', icon: '👁' },
  { event: 'start', description: 'Video playback begins (0%)', icon: '▶' },
  { event: 'firstQuartile', description: '25% of video watched', icon: '¼' },
  { event: 'midpoint', description: '50% of video watched', icon: '½' },
  { event: 'thirdQuartile', description: '75% of video watched', icon: '¾' },
  { event: 'complete', description: '100% of video watched', icon: '✓' },
  { event: 'click', description: 'User clicked through', icon: '🔗' },
]

export const measurementVendors = [
  { name: 'Integral Ad Science', key: 'ias', type: 'Viewability + Brand Safety', cpm: 0.02, omid: true },
  { name: 'Moat by Oracle', key: 'moat', type: 'Attention + Viewability', cpm: 0.03, omid: true },
  { name: 'DoubleVerify', key: 'doubleverify', type: 'Brand Safety + Fraud', cpm: 0.025, omid: true },
]
