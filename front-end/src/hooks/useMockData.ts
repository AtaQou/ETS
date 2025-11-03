import { useEffect } from "react";
import useEyeTrackingStore from "store/store";
import { GazeData } from "types/AppTypes";
import { testData } from "../utils/test.js";
import { forEach } from "lodash";

const sample: GazeData = {
  _id: 279902541957,
  _index: "ets",
  _score: 1,
  device_time_stamp: "1,454,059,042",
  left_gaze_origin_in_trackbox_coordinate_system: [0.572, 0.538, 0.373],
  left_gaze_origin_in_user_coordinate_system: [-22.924, -38.571],
  left_gaze_origin_validity: 1,
  left_gaze_point_in_user_coordinate_system: [-19.204, 120.623],
  left_gaze_point_on_display_area: [0.464, 0.607],
  left_gaze_point_validity: 1,
  left_pupil_diameter: 2.82,
  left_pupil_validity: 1,
  right_gaze_origin_in_trackbox_coordinate_system: [0.377, 0.523, 0.356],
  right_gaze_origin_in_user_coordinate_system: [38.167, -34.861, 587.6],
  right_gaze_origin_validity: 1,
  right_gaze_point_in_user_coordinate_system: [-19.204, 120.623],
  right_gaze_point_on_display_area: [0.46, 0.599],
  right_gaze_point_validity: 2.82,
  right_pupil_diameter: [-21.045, 122.713, 44.664],
  right_pupil_validity: [0.46, 0.599],
  system_time_stamp: 1,
};

const useMockData = () => {
  const { accumulateData } = useEyeTrackingStore();

  useEffect(() => {
    const intervalId = setInterval(() => {
      accumulateData(sample);
    }, 3.33);

    return () => {
      clearInterval(intervalId);
    };
  }, [accumulateData]);

  // useEffect(() => {
  //   let intervalId: NodeJS.Timer;
  //   let currentIndex = 0;

  //   const sendTestData = () => {
  //     if (currentIndex < testData.length) {
  //       const dataPoint = testData[currentIndex];
  //       if (!dataPoint.includes("NaN")) {
  //         accumulateData(JSON.parse(dataPoint));
  //         currentIndex++;
  //       }
  //     }
  //   };

  //   intervalId = setInterval(sendTestData, 1000 / 300);

  //   return () => {
  //     clearInterval(intervalId as any);
  //   };
  // }, [accumulateData]);
};

export default useMockData;
