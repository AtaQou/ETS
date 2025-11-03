import React, { useContext, useState, KeyboardEvent } from "react";
import axios from "axios";
import { Context } from "../context/Context";
import { useSnackbar } from "../hooks/useSnackbar";
import { apiURL, dark_primary, dark_secondary, light_primary, light_secondary } from "../utils/consts";
import { getFontColorSecondary } from "../utils/functions";
import Button from "./ui/Button";

const UserProfile: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { setUserInfo, userSettingsApi } = useContext(Context);
  const [error, setError] = useState("");
  const { triggerSnackbar } = useSnackbar();
  const isDarkTheme = userSettingsApi.theme === "dark";

  const handleEnterPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      if (isLogin) {
        loginUser();
      } else {
        createUser();
      }
    }
  };

  const createUser = () => {
    axios
      .post(`${apiURL}/create-profile`, {
        username,
        password,
      })
      .then((res) => {
        if (res.status === 200) {
          setIsLogin(true);
          setUsername("");
          setPassword("");
          setError("");
          triggerSnackbar({
            message: "User created successfully!",
            status: "success",
            open: true,
          });
        }
      })
      .catch((err) => {
        if (err.response.status === 400) {
          setError(err.response.data.message);
          triggerSnackbar({
            message: "Failed to create user!",
            status: "error",
            open: true,
          });
        }
      });
  };

  const loginUser = () => {
    axios
      .post(`${apiURL}/login`, {
        username,
        password,
      })
      .then((res) => {
        if (res.status === 200) {
          setUserInfo?.({
            isLoggedIn: true,
            userID: res.data.userID,
            username: res.data.username,
          });
        }
      })
      .catch((err) => {
        console.error({ err });
        if (err.response.status === 400) {
          setError(err.response.data.message);
        }
      });
  };

  const toggleLogin = () => {
    setIsLogin((prev) => !prev);
  };

  return (
    <div
      className={`flex flex-col items-center h-screen`}
      style={
        isDarkTheme
          ? {
              backgroundColor: dark_primary,
            }
          : {
              backgroundColor: light_secondary,
            }
      }
    >
      <div className='xl:mb-[100px] xl:mt-[100px] lg:mb-[30px]'>
        <img src={isDarkTheme ? "./logo5.png" : "./logo_light.png"} alt='' className='h-32' />
      </div>
      <div
        className='p-8  rounded shadow-md w-96 flex flex-col justify-between items-center'
        style={
          isDarkTheme
            ? {
                backgroundColor: dark_secondary,
              }
            : {
                backgroundColor: light_primary,
              }
        }
      >
        <h2 className='mb-8 text-3xl text-blue-600 text-center'>{isLogin ? "Login" : "Create profile"}</h2>
        <input
          className='mb-4 w-full px-3 py-2 border rounded-md'
          type='text'
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={handleEnterPress}
          placeholder='Username'
        />
        <input
          className='mb-4 w-full px-3 py-2 border rounded-md'
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={handleEnterPress}
          placeholder='Password'
        />
        {error && <div className='text-red-700 flex justify-center pb-2'>{error}</div>}
        {isLogin ? (
          <Button
            className={`w-full px-3 py-2 bg-green-600  rounded-md hover:bg-green-700`}
            style={{ color: light_secondary }}
            onClick={loginUser}
          >
            Login
          </Button>
        ) : (
          <Button
            className={`w-full px-3 py-2 bg-green-600 rounded-md hover:bg-green-700`}
            style={{ color: light_secondary }}
            onClick={createUser}
          >
            Create Profile
          </Button>
        )}
        {isLogin ? (
          <div className='my-4' style={{ color: getFontColorSecondary(isDarkTheme) }}>
            Don't have a profile?
            <Button
              className='ml-2 hover:text-blue-600'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
              onClick={toggleLogin}
            >
              Create Profile
            </Button>
          </div>
        ) : (
          <div className='my-4' style={{ color: getFontColorSecondary(isDarkTheme) }}>
            Already have a profile?
            <Button
              className='ml-2 hover:text-blue-600'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
              onClick={toggleLogin}
            >
              Login
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserProfile;
