﻿USE [master]
GO
/****** Object:  Database [LambdaComplex]    Script Date: 29-04-2024 11:56:31 PM ******/
CREATE DATABASE [LambdaComplex]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'LambdaComplex', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\LambdaComplex.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'LambdaComplex_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\LambdaComplex_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [LambdaComplex] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [LambdaComplex].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [LambdaComplex] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [LambdaComplex] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [LambdaComplex] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [LambdaComplex] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [LambdaComplex] SET ARITHABORT OFF 
GO
ALTER DATABASE [LambdaComplex] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [LambdaComplex] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [LambdaComplex] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [LambdaComplex] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [LambdaComplex] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [LambdaComplex] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [LambdaComplex] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [LambdaComplex] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [LambdaComplex] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [LambdaComplex] SET  ENABLE_BROKER 
GO
ALTER DATABASE [LambdaComplex] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [LambdaComplex] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [LambdaComplex] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [LambdaComplex] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [LambdaComplex] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [LambdaComplex] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [LambdaComplex] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [LambdaComplex] SET RECOVERY FULL 
GO
ALTER DATABASE [LambdaComplex] SET  MULTI_USER 
GO
ALTER DATABASE [LambdaComplex] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [LambdaComplex] SET DB_CHAINING OFF 
GO
ALTER DATABASE [LambdaComplex] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [LambdaComplex] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [LambdaComplex] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [LambdaComplex] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'LambdaComplex', N'ON'
GO
ALTER DATABASE [LambdaComplex] SET QUERY_STORE = ON
GO
ALTER DATABASE [LambdaComplex] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [LambdaComplex]
GO
/****** Object:  User [Server_Admin]    Script Date: 29-04-2024 11:56:32 PM ******/
CREATE USER [Server_Admin] FOR LOGIN [Server_Admin] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  Table [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl](
	[ID] [varchar](36) NOT NULL,
	[EventDescription] [varchar](max) NULL,
	[EventDate] [datetime] NULL,
	[CreatedBy] [varchar](36) NOT NULL,
	[ModifiedBy] [varchar](36) NOT NULL,
	[IsDeleted] [bit] NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[EventPriority] [varchar](4) NULL,
	[EventName] [varchar](200) NULL,
	[EventTime] [varchar](10) NULL,
	[IsExpired] [bit] NULL,
 CONSTRAINT [PK__LambdaCo__3214EC278A076386] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_File_Trn_Tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_File_Trn_Tbl](
	[ID] [varchar](36) NULL,
	[UserID] [varchar](36) NOT NULL,
	[RecordID] [varchar](36) NOT NULL,
	[FileName] [varchar](200) NOT NULL,
	[FileType] [varchar](200) NOT NULL,
	[StoredFileName] [varchar](500) NOT NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Goal_Changes_Trn_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl](
	[RecordId] [varchar](36) NULL,
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[AssignedTo] [varchar](36) NULL,
	[ReportingStatus] [varchar](15) NULL,
	[Version] [int] NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[IsStable] [bit] NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL,
	[ParentID] [varchar](36) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Goal_Mst_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Goal_Mst_tbl](
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[AssignedTo] [varchar](36) NULL,
	[ReportingStatus] [varchar](15) NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[Version] [int] NULL,
	[IsStable] [bit] NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL,
	[ParentID] [varchar](36) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl](
	[RecordId] [varchar](36) NULL,
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[AssignedTo] [varchar](36) NULL,
	[ReportingStatus] [varchar](15) NULL,
	[Version] [int] NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[IsStable] [bit] NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL,
	[ParentID] [varchar](36) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_MileStone_Mst_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl](
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[AssignedTo] [varchar](36) NULL,
	[ReportingStatus] [varchar](15) NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[IsStable] [bit] NULL,
	[Version] [int] NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL,
	[ParentID] [varchar](36) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Project_Changes_Trn_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl](
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[ReportingStatus] [varchar](15) NULL,
	[IsStable] [bit] NULL,
	[Version] [int] NULL,
	[RecordID] [varchar](36) NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Project_Mst_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Project_Mst_tbl](
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[IsStable] [bit] NULL,
	[Version] [int] NULL,
	[ReportingStatus] [varchar](15) NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Task_Changes_Trn_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl](
	[RecordId] [varchar](36) NULL,
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[AssignedTo] [varchar](36) NULL,
	[ReportingStatus] [varchar](15) NULL,
	[Version] [int] NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[IsStable] [bit] NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL,
	[ParentID] [varchar](36) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Task_Mst_tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Task_Mst_tbl](
	[ID] [varchar](36) NULL,
	[Name] [varchar](200) NULL,
	[Description] [varchar](max) NULL,
	[RunningStatus] [int] NULL,
	[AssignedTo] [varchar](36) NULL,
	[ReportingStatus] [varchar](15) NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[IsStable] [bit] NULL,
	[Version] [int] NULL,
	[Deadline] [datetime] NULL,
	[Rating] [int] NULL,
	[Remarks] [varchar](max) NULL,
	[ParentID] [varchar](36) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_Team_Mst_Tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_Team_Mst_Tbl](
	[ID] [varchar](36) NOT NULL,
	[TeamName] [varchar](200) NULL,
	[TeamDescription] [varchar](max) NULL,
	[LeaderID] [varchar](36) NOT NULL,
	[ProjectID] [varchar](36) NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_TeamMember_Trn_Tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_TeamMember_Trn_Tbl](
	[ID] [varchar](36) NOT NULL,
	[TeamID] [varchar](36) NOT NULL,
	[TeamMemberID] [varchar](36) NOT NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NULL,
	[ModifiedBy] [varchar](36) NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_User_Mst_Tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_User_Mst_Tbl](
	[ID] [varchar](36) NOT NULL,
	[FirstName] [varchar](100) NOT NULL,
	[LastName] [varchar](100) NOT NULL,
	[Password] [varchar](500) NOT NULL,
	[UserName] [varchar](100) NOT NULL,
	[EmailID] [varchar](200) NOT NULL,
	[IsDeleted] [bit] NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL,
	[Role] [varchar](20) NULL,
	[MobileNumber] [char](10) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LambdaComplex_WorkTimeline_Trn_Tbl]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LambdaComplex_WorkTimeline_Trn_Tbl](
	[ID] [varchar](36) NULL,
	[Message] [varchar](500) NOT NULL,
	[RecordID] [varchar](36) NOT NULL,
	[IsDeleted] [bit] NULL,
	[CreatedBy] [varchar](36) NOT NULL,
	[ModifiedBy] [varchar](36) NOT NULL,
	[CreatedOn] [datetime] NULL,
	[ModifiedOn] [datetime] NULL
) ON [PRIMARY]
GO
INSERT [dbo].[LambdaComplex_User_Mst_Tbl] ([ID], [FirstName], [LastName], [Password], [UserName], [EmailID], [IsDeleted], [CreatedOn], [ModifiedOn], [Role], [MobileNumber]) VALUES (newid(), N'Root', N'Admin', HASHBYTES('SHA2_256','LC_Admin@2024'), N'Root.Admin', N'Root.Admin@gmail.com', 0, getdate(), getdate(), N'Admin', N'1234567890')
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaComple__ID__49C3F6B7]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__Event__4AB81AF0]  DEFAULT ('') FOR [EventDescription]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__Event__4BAC3F29]  DEFAULT (getdate()) FOR [EventDate]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__4CA06362]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__4D94879B]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__4E88ABD4]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__Event__4F7CD00D]  DEFAULT ('MID') FOR [EventPriority]
GO
ALTER TABLE [dbo].[LambdaComplex_CalendarEvent_Trn_Tbl] ADD  CONSTRAINT [DF__LambdaCom__IsExp__4D5F7D71]  DEFAULT ((0)) FOR [IsExpired]
GO
ALTER TABLE [dbo].[LambdaComplex_File_Trn_Tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_File_Trn_Tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_File_Trn_Tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_File_Trn_Tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Goal_Changes_Trn_tbl_ID]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaComp__Name__52593CB8]  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Descr__534D60F1]  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Runni__5441852A]  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Repor__5535A963]  DEFAULT ((0)) FOR [ReportingStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__versi__5629CD9C]  DEFAULT ((1)) FOR [Version]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__571DF1D5]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__5812160E]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__59063A47]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Goal_Changes_Trn_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaComple__ID__59FA5E80]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaComp__Name__5AEE82B9]  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Descr__5BE2A6F2]  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Runni__5CD6CB2B]  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Repor__5DCAEF64]  DEFAULT ((0)) FOR [ReportingStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__5EBF139D]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__5FB337D6]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__60A75C0F]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Goal_Mst_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Goal_Mst_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_MileStone_Changes_Trn_tbl_ID]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaComp__Name__628FA481]  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Descr__6383C8BA]  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Runni__6477ECF3]  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Repor__656C112C]  DEFAULT ((0)) FOR [ReportingStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__versi__66603565]  DEFAULT ((1)) FOR [Version]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__6754599E]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__68487DD7]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__693CA210]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_MileStone_Changes_Trn_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaComple__ID__6A30C649]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaComp__Name__6B24EA82]  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Descr__6C190EBB]  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Runni__6D0D32F4]  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Repor__6E01572D]  DEFAULT ((0)) FOR [ReportingStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__6EF57B66]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__6FE99F9F]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__70DDC3D8]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_MileStone_Mst_tbl] ADD  CONSTRAINT [DF_LambdaComplex_MileStone_Mst_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Project_Changes_Trn_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Project_Mst_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Project_Mst_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Task_Changes_Trn_tbl_ID]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaComp__Name__00200768]  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Descr__01142BA1]  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Runni__02084FDA]  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Repor__02FC7413]  DEFAULT ((0)) FOR [ReportingStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__versi__03F0984C]  DEFAULT ((1)) FOR [Version]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__04E4BC85]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__05D8E0BE]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__06CD04F7]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Changes_Trn_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Task_Changes_Trn_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaComple__ID__07C12930]  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaComp__Name__08B54D69]  DEFAULT ('') FOR [Name]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Descr__09A971A2]  DEFAULT ('') FOR [Description]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Runni__0A9D95DB]  DEFAULT ((0)) FOR [RunningStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Repor__0B91BA14]  DEFAULT ((0)) FOR [ReportingStatus]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__IsDel__0C85DE4D]  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Creat__0D7A0286]  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF__LambdaCom__Modif__0E6E26BF]  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Task_Mst_tbl] ADD  CONSTRAINT [DF_LambdaComplex_Task_Mst_tbl_Rating]  DEFAULT ((5)) FOR [Rating]
GO
ALTER TABLE [dbo].[LambdaComplex_Team_Mst_Tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_Team_Mst_Tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_Team_Mst_Tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_Team_Mst_Tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_TeamMember_Trn_Tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_TeamMember_Trn_Tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_TeamMember_Trn_Tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_TeamMember_Trn_Tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_User_Mst_Tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_User_Mst_Tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_User_Mst_Tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_User_Mst_Tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_WorkTimeline_Trn_Tbl] ADD  DEFAULT (newid()) FOR [ID]
GO
ALTER TABLE [dbo].[LambdaComplex_WorkTimeline_Trn_Tbl] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[LambdaComplex_WorkTimeline_Trn_Tbl] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[LambdaComplex_WorkTimeline_Trn_Tbl] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
/****** Object:  StoredProcedure [dbo].[LambdaComplex_ClearDB_SP]    Script Date: 29-04-2024 11:56:32 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[LambdaComplex_ClearDB_SP]
as 
begin
	delete from LambdaComplex_CalendarEvent_Trn_Tbl;
	delete from LambdaComplex_File_Trn_Tbl;
	delete from LambdaComplex_Goal_Changes_Trn_tbl;
	delete from LambdaComplex_Goal_Mst_tbl;
	delete from LambdaComplex_Project_Changes_Trn_tbl;
	delete from LambdaComplex_Project_Mst_tbl;
	delete from LambdaComplex_Task_Changes_Trn_tbl;
	delete from LambdaComplex_Task_Mst_tbl;
	delete from LambdaComplex_MileStone_Changes_Trn_tbl;
	delete from LambdaComplex_MileStone_Mst_tbl;
	delete from LambdaComplex_Team_Mst_Tbl;
	delete from LambdaComplex_TeamMember_Trn_Tbl;
	delete from LambdaComplex_WorkTimeline_Trn_Tbl;
end
GO
USE [master]
GO
ALTER DATABASE [LambdaComplex] SET  READ_WRITE 
GO
