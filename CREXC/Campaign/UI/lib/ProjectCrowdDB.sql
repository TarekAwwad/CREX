-- phpMyAdmin SQL Dump
-- version 4.4.9
-- http://www.phpmyadmin.net
--
-- Host: localhost:8889
-- Generation Time: Oct 26, 2017 at 11:11 AM
-- Server version: 5.5.42
-- PHP Version: 5.6.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ProjectCrowdDB`
--

-- --------------------------------------------------------

--
-- Table structure for table `contribution`
--

CREATE TABLE `contribution` (
  `ID` varchar(255) NOT NULL,
  `TaskID` varchar(16) CHARACTER SET ascii NOT NULL,
  `WorkerID` varchar(16) CHARACTER SET ascii NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Content` text CHARACTER SET ascii NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contribution`
--

INSERT INTO `contribution` (`ID`, `TaskID`, `WorkerID`, `TimeStamp`, `Content`) VALUES
('0', 'a9', '1231231', '2017-10-26 09:08:19', '{a9_task-1_op:0,a9_task-1_ft_0:v,a9_task-1_ft_1:v,a9_task-1_ft_2:v,a9_task-2_op:1,a9_task-2_ft_0:v,a9_task-2_ft_1:v,a9_task-2_ft_2:v,}'),
('1', 'a9', '45121', '2017-10-26 08:33:41', '{a9_task-1_op:0,a9_task-1_ft_0:ytyt,a9_task-1_ft_1:rtrt,a9_task-1_ft_2:erer,a9_task-2_op:0,a9_task-2_ft_0:wewe,a9_task-2_ft_1:qwqw,a9_task-2_ft_2:aqaq,}'),
('2', 'a9', '1231231', '2017-10-26 09:05:53', '{a9_task-1_op:0,a9_task-1_ft_0:v,a9_task-1_ft_1:v,a9_task-1_ft_2:v,a9_task-2_op:1,a9_task-2_ft_0:v,a9_task-2_ft_1:v,a9_task-2_ft_2:v,}'),
('unit--a9-1231231', 'a9', '1231231', '2017-10-26 09:10:33', '{a9_task-1_op:0,a9_task-1_ft_0:v,a9_task-1_ft_1:v,a9_task-1_ft_2:v,a9_task-2_op:1,a9_task-2_ft_0:v,a9_task-2_ft_1:v,a9_task-2_ft_2:v,}'),
('unit-a9-1231231', 'a9', '1231231', '2017-10-26 09:10:54', '{a9_task-1_op:0,a9_task-1_ft_0:v,a9_task-1_ft_1:v,a9_task-1_ft_2:v,a9_task-2_op:1,a9_task-2_ft_0:v,a9_task-2_ft_1:v,a9_task-2_ft_2:v,}'),
('unita91231231', 'a9', '1231231', '2017-10-26 09:09:41', '{a9_task-1_op:0,a9_task-1_ft_0:v,a9_task-1_ft_1:v,a9_task-1_ft_2:v,a9_task-2_op:1,a9_task-2_ft_0:v,a9_task-2_ft_1:v,a9_task-2_ft_2:v,}');

-- --------------------------------------------------------

--
-- Table structure for table `contributor`
--

CREATE TABLE `contributor` (
  `CID` varchar(16) CHARACTER SET ascii NOT NULL,
  `Age` varchar(16) CHARACTER SET ascii NOT NULL,
  `Gender` varchar(16) CHARACTER SET ascii NOT NULL,
  `Education_l` varchar(255) CHARACTER SET ascii NOT NULL,
  `Education_d` varchar(255) CHARACTER SET ascii NOT NULL,
  `Work_l` varchar(255) CHARACTER SET ascii NOT NULL,
  `Work_d` varchar(255) CHARACTER SET ascii NOT NULL,
  `Country` varchar(255) CHARACTER SET ascii NOT NULL,
  `Language_n` varchar(255) CHARACTER SET ascii NOT NULL,
  `Language_o` varchar(255) CHARACTER SET ascii NOT NULL,
  `Interests` varchar(255) CHARACTER SET ascii NOT NULL,
  `Rating_1` varchar(255) CHARACTER SET ascii NOT NULL,
  `Rating_2` varchar(255) CHARACTER SET ascii NOT NULL,
  `Rating_3` varchar(255) CHARACTER SET ascii NOT NULL,
  `Rating_4` varchar(255) CHARACTER SET ascii NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contributor`
--

INSERT INTO `contributor` (`CID`, `Age`, `Gender`, `Education_l`, `Education_d`, `Work_l`, `Work_d`, `Country`, `Language_n`, `Language_o`, `Interests`, `Rating_1`, `Rating_2`, `Rating_3`, `Rating_4`) VALUES
('', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
('1', 'More than 60', 'Female', 'Algeria', 'School', 'Business Studies, Management Science', 'less than 3 years', 'Academic/educator', 'Albanian', 'Arabic', 'Arts and Entertainment', 'Arts and Entertainment', '', '', ''),
('12', 'less than 16', 'Female', 'Angola', 'High school', 'Education, Teacher Training', 'less than 3 years', 'Scientist', 'Afrikaans', 'Awadhi', 'Shopping', 'Shopping', '', '', ''),
('1201', 'More than 60', 'Female', 'Algeria', 'School', 'Business Studies, Management Science', 'less than 3 years', 'Academic/educator', 'Albanian', 'Arabic', 'Arts and Entertainment', 'Arts and Entertainment', '', '', ''),
('12011', 'More than 60', 'Female', 'Algeria', 'School', 'Business Studies, Management Science', 'less than 3 years', 'Academic/educator', 'Albanian', 'Arabic', 'Arts and Entertainment', 'Arts and Entertainment', '', '', ''),
('120111', 'More than 60', 'Female', 'Algeria', 'School', 'Business Studies, Management Science', 'less than 3 years', 'Academic/educator', 'Albanian', 'Arabic', 'Arts and Entertainment', 'Arts and Entertainment', '', '', ''),
('1201111', 'More than 60', 'Female', 'Algeria', 'School', 'Business Studies, Management Science', 'less than 3 years', 'Academic/educator', 'Albanian', 'Arabic', 'Arts and Entertainment', 'Arts and Entertainment', '', '', ''),
('12011112', 'More than 60', 'Female', 'Algeria', 'School', 'Business Studies, Management Science', 'less than 3 years', 'Academic/educator', 'Albanian', 'Arabic', 'Arts and Entertainment', 'Arts and Entertainment', '', '', ''),
('122', 'More than 60', 'Female', 'Albania', 'High school', 'Sciences Architecture, Urban and Regional Planning', 'less than 10 years', 'Artist', 'Albanian', 'Azerbaijani', 'Finance', 'Finance', '', '', ''),
('1231', '21-25', 'Male', 'University', 'Mathematics, Informatics', 'less than 10 years', 'Homemaker', 'Andorra', 'Bhojpuri', 'Basque', 'Finance', '5', '2', '3', '3'),
('12312', '21-25', 'Male', 'University', 'Mathematics, Informatics', 'less than 10 years', 'Homemaker', 'Andorra', 'Bhojpuri', 'Basque', 'Finance', '5', '2', '3', '3'),
('123121', '21-25', 'Male', 'University', 'Mathematics, Informatics', 'less than 10 years', 'Homemaker', 'Andorra', 'Bhojpuri', 'Basque', 'Finance', '5', '2', '3', '3'),
('1231212', '21-25', 'Male', 'University', 'Mathematics, Informatics', 'less than 10 years', 'Homemaker', 'Andorra', 'Bhojpuri', 'Basque', 'Finance', '5', '2', '3', '3'),
('12312127', '21-25', 'Male', 'University', 'Mathematics, Informatics', 'less than 10 years', 'Homemaker', 'Andorra', 'Bhojpuri', 'Basque', 'Finance', '5', '2', '3', '3'),
('123121271', '21-25', 'Male', 'University', 'Mathematics, Informatics', 'less than 10 years', 'Homemaker', 'Andorra', 'Bhojpuri', 'Basque', 'Finance', '5', '2', '3', '3'),
('1231231', 'less than 16', 'Female', 'High school', 'Art and Design', 'less than 10 years', 'Clerical/admin', 'Albania', 'Armenian', 'Burmese', 'Finance', '5', '2', '3', '2'),
('123123122', '16-20', 'Male', 'Algeria', 'University', 'Geography, Geology', 'less than 10 years', 'Artist', 'Arabic', 'Awadhi', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('123123123', '26-30', 'Male', 'Angola', 'High school', 'Engineering, Technology', 'fresh graduated', 'Clerical/admin', 'Arabic', 'Afrikaans', 'Business and Industrial', 'Business and Industrial', '', '', ''),
('123123124', '16-20', 'Male', 'Algeria', 'University', 'Geography, Geology', 'less than 10 years', 'Artist', 'Arabic', 'Awadhi', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('123123125', '46-50', 'Male', 'Belarus', 'Doctoral studies', 'Sciences Architecture, Urban and Regional Planning', 'less than 10 years', 'Academic/educator', 'Afrikaans', 'Burmese', 'Beauty and Fitness', 'Beauty and Fitness', '', '', ''),
('123147', '31-35', 'Male', 'Algeria', 'High school', 'Humanities', 'fresh graduated', 'Academic/educator', 'Awadhi', 'Awadhi', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('123258', '31-35', 'Male', 'Algeria', 'High school', 'Humanities', 'fresh graduated', 'Academic/educator', 'Awadhi', 'Awadhi', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('123369', 'less than 16', 'Female', 'Angola', 'University', 'Humanities', 'less than 3 years', 'Clerical/admin', 'Armenian', 'Bengali', 'Finance', 'Finance', '', '', ''),
('123456', '26-30', 'Male', 'Lebanon', 'Doctoral studies', 'Mathematics, Informatics', 'less than 10 years', 'Scientist', 'Arabic', 'French', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('12451245', 'Female', '21-25', 'Tokelau', 'Business Studies, Management Science', 'High school', 'Retired', 'less than 10 years', 'Croatian', 'Bosnian', 'Jobs and Education', '3', '', '', ''),
('1278', 'less than 16', 'Female', 'Afghanistan', 'University', 'Agriculture Sciences', 'less than 3 years', 'Artist', 'Albanian', 'Afrikaans', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('131314', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('1313141', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('13131411', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('131314112', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('14789', '21-25', 'Male', 'Congo  Democratic Republic of the (Zaire)', 'University', 'Geography, Geology', 'less than 10 years', 'Customer service', 'Armenian', 'Azerbaijani', 'Business and Industrial', 'Business and Industrial', '', '', ''),
('159123', '31-35', 'Male', 'Anguilla', 'High school', 'Sciences Architecture, Urban and Regional Planning', 'less than 10 years', 'Academic/educator', 'Bosnian', 'Czech', 'Beauty and Fitness', 'Beauty and Fitness', '', '', ''),
('159753', '31-35', 'Male', 'Algeria', 'High school', 'Humanities', 'fresh graduated', 'Academic/educator', 'Awadhi', 'Awadhi', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('159789', '36-40', 'Female', 'Kiribati', 'University', 'Law', 'more than 10 years', 'Executive/managerial', 'Catalan', 'Bhojpuri', 'Online Communities', 'Online Communities', '', '', ''),
('3', 'More than 60', 'Male', 'Afghanistan', 'High school', 'Humanities', 'less than 3 years', 'Artist', 'Arabic', 'Azerbaijani', 'Books and Literature', 'Books and Literature', '', '', ''),
('31314112', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('33', 'More than 60', 'Male', 'Afghanistan', 'High school', 'Humanities', 'less than 3 years', 'Artist', 'Arabic', 'Azerbaijani', 'Books and Literature', 'Books and Literature', '', '', ''),
('33122', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('3314112', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('33141124', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('331411242', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('33142', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('331422', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('3314223', '16-20', 'Female', 'University', 'Languages and Philological Sciences', 'less than 10 years', 'Lawyer', 'Armenia', 'Basque', 'Basque', 'Computers and Electronics', '5', '4', '2', '3'),
('344', '344', 'Male', '31-35', 'Andorra', 'Business Studies, Management Science', 'High school', 'Customer service', 'more than 10 years', 'Bosnian', 'Bosnian', 'Bosnian', '', '', ''),
('3443', 'Male', '31-35', 'Andorra', 'Business Studies, Management Science', 'High school', 'Customer service', 'more than 10 years', 'Bosnian', 'Bosnian', 'Law and Government', '3', '', '', ''),
('34433', 'Male', 'Andorra', 'High school', 'Business Studies, Management Science', 'more than 10 years', 'Customer service', 'Bosnian', 'Bosnian', 'Law and Government', 'Law and Government', 'Law and Government', '', '', ''),
('45', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('451', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('4511', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('45111', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('451112', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('4511127', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('45112', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('451121', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('45121', 'less than 16', 'Male', 'School', 'Agriculture Sciences', 'fresh graduated', 'Academic/educator', 'Afghanistan', 'Afrikaans', 'Afrikaans', 'Arts and Entertainment', '1', '2', '3', '4'),
('456147', '31-35', 'Male', 'Algeria', 'High school', 'Humanities', 'fresh graduated', 'Academic/educator', 'Awadhi', 'Awadhi', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('456258', '31-35', 'Male', 'Algeria', 'High school', 'Humanities', 'fresh graduated', 'Academic/educator', 'Awadhi', 'Awadhi', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('456369', '31-35', 'Male', 'Algeria', 'High school', 'Humanities', 'fresh graduated', 'Academic/educator', 'Awadhi', 'Awadhi', 'Autos and Vehicles', 'Autos and Vehicles', '', '', ''),
('456785', '16-20', 'Female', 'Algeria', 'Doctoral studies', 'Art and Design', 'less than 10 years', 'Customer service', 'Arabic', 'Arabic', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('4567850', '16-20', 'Female', 'Algeria', 'Doctoral studies', 'Art and Design', 'less than 10 years', 'Customer service', 'Arabic', 'Arabic', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('45678501', '16-20', 'Female', 'Algeria', 'Doctoral studies', 'Art and Design', 'less than 10 years', 'Customer service', 'Arabic', 'Arabic', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('456789', '21-25', 'Female', 'Brazil', 'Doctoral studies', 'Humanities', 'less than 3 years', 'Executive/managerial', 'Albanian', 'Arabic', 'Beauty and Fitness', 'Beauty and Fitness', '', '', ''),
('754286', '36-40', 'Female', 'Angola', 'University', 'Business Studies, Management Science', 'less than 10 years', 'College/grad student', 'Albanian', 'Arabic', 'Books and Literature', 'Books and Literature', '', '', ''),
('7542868', '41-45', 'Female', 'Gibraltar', 'High school', 'Geography, Geology', 'less than 3 years', 'Homemaker', 'Albanian', 'Belarusian', 'Hobbies and Leisure', 'Hobbies and Leisure', '', '', ''),
('75428684', '41-45', 'Female', 'Gibraltar', 'High school', 'Geography, Geology', 'less than 3 years', 'Homemaker', 'Albanian', 'Belarusian', 'Hobbies and Leisure', 'Hobbies and Leisure', '', '', ''),
('7676', '46-50', 'Male', 'High school', 'Art and Design', 'less than 3 years', 'Scientist', 'Bulgaria', 'French', 'Hungarian', 'Home and Garden', '5', '4', '4', '4'),
('76761', '46-50', 'Male', 'High school', 'Art and Design', 'less than 3 years', 'Scientist', 'Bulgaria', 'French', 'Hungarian', 'Home and Garden', '5', '4', '4', '4'),
('767611', '46-50', 'Male', 'High school', 'Art and Design', 'less than 3 years', 'Scientist', 'Bulgaria', 'French', 'Hungarian', 'Home and Garden', '5', '4', '4', '4'),
('7676111', '46-50', 'Male', 'High school', 'Art and Design', 'less than 3 years', 'Scientist', 'Bulgaria', 'French', 'Hungarian', 'Home and Garden', '5', '4', '4', '4'),
('789123', 'less than 16', 'Female', 'Angola', 'University', 'Humanities', 'less than 3 years', 'Clerical/admin', 'Armenian', 'Bengali', 'Finance', 'Finance', '', '', ''),
('789147', 'less than 16', 'Female', 'Angola', 'University', 'Humanities', 'less than 3 years', 'Clerical/admin', 'Armenian', 'Bengali', 'Finance', 'Finance', '', '', ''),
('789258', 'less than 16', 'Female', 'Angola', 'University', 'Humanities', 'less than 3 years', 'Clerical/admin', 'Armenian', 'Bengali', 'Finance', 'Finance', '', '', ''),
('789369', 'less than 16', 'Female', 'Angola', 'University', 'Humanities', 'less than 3 years', 'Clerical/admin', 'Armenian', 'Bengali', 'Finance', 'Finance', '', '', ''),
('789456', 'less than 16', 'Female', 'Angola', 'University', 'Humanities', 'less than 3 years', 'Clerical/admin', 'Armenian', 'Bengali', 'Finance', 'Finance', '', '', ''),
('95759', '41-45', 'Male', 'Egypt', 'University', 'Humanities', 'more than 10 years', 'Customer service', 'Polish', 'Awadhi', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('957591', '41-45', 'Male', 'Egypt', 'University', 'Humanities', 'more than 10 years', 'Customer service', 'Polish', 'Awadhi', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('9575911', '41-45', 'Male', 'Egypt', 'University', 'Humanities', 'more than 10 years', 'Customer service', 'Polish', 'Awadhi', 'Computers and Electronics', 'Computers and Electronics', '', '', ''),
('99', 'More than 60', 'Male', 'Afghanistan', 'High school', 'Humanities', 'less than 3 years', 'Artist', 'Arabic', 'Azerbaijani', 'Books and Literature', 'Books and Literature', '', '', ''),
('991', 'More than 60', 'Male', 'Afghanistan', 'High school', 'Humanities', 'less than 3 years', 'Artist', 'Arabic', 'Azerbaijani', 'Books and Literature', 'Books and Literature', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `ID` varchar(16) CHARACTER SET ascii NOT NULL,
  `Content` text CHARACTER SET ascii NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contribution`
--
ALTER TABLE `contribution`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `contributor`
--
ALTER TABLE `contributor`
  ADD PRIMARY KEY (`CID`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
