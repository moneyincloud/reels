import { AbsoluteFill, Composition, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

// @moneyincloud reel defaults: 1080x1920, 30 fps. Smoke test for the toolchain.
export const MyComposition = () => (
  <Composition id="Reel" component={SmokeTest} durationInFrames={90} fps={30} width={1080} height={1920} />
);

const EASE_IN = Easing.bezier(0.16, 1, 0.3, 1);

export const SmokeTest: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - 10, fps, config: { damping: 12 } });
  const rise = interpolate(frame, [0, 16], [115, 0], { extrapolateRight: "clamp", easing: EASE_IN });
  return (
    <AbsoluteFill style={{ background: "#F4FCF6", alignItems: "center", justifyContent: "center", fontFamily: "sans-serif" }}>
      <div style={{ overflow: "hidden" }}>
        <div style={{ transform: `translateY(${rise}%)`, fontSize: 120, fontWeight: 900, color: "#10221A" }}>₹1 LAKH</div>
      </div>
      <div style={{ transform: `scale(${pop})`, marginTop: 40, background: "#16965A", color: "white", fontSize: 64, fontWeight: 800, padding: "20px 44px", borderRadius: 999 }}>
        Remotion ready
      </div>
    </AbsoluteFill>
  );
};
