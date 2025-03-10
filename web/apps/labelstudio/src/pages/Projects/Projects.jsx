import React, { useState, useEffect } from "react";
import { useParams as useRouterParams } from "react-router";
import { Redirect } from "react-router-dom";
import { Button } from "../../components";
import { Oneof } from "../../components/Oneof/Oneof";
import { Spinner } from "../../components/Spinner/Spinner";
import { ApiContext } from "../../providers/ApiProvider";
import { useContextProps } from "../../providers/RoutesProvider";
import { useAbortController } from "../../hooks/useAbortController";
import { Block, Elem } from "../../utils/bem";
import { FF_DEV_2575, isFF } from "../../utils/feature-flags";
import { CreateProject } from "../CreateProject/CreateProject";
import { DataManagerPage } from "../DataManager/DataManager";
import { SettingsPage } from "../Settings";
import { useConfig } from "../../providers/ConfigProvider";
import languages from "./languages.json";
import "./Projects.styl";
import { EmptyProjectsList, ProjectsList, ProjectLanguageSelector } from "./ProjectsList";

const getCurrentPage = () => {
  const pageNumberFromURL = new URLSearchParams(location.search).get("page");

  return pageNumberFromURL ? Number.parseInt(pageNumberFromURL) : 1;
};

export const ProjectsPage = () => {
  const api = React.useContext(ApiContext);
  const abortController = useAbortController();
  const [projectsList, setProjectsList] = React.useState([]);
  const [networkState, setNetworkState] = React.useState(null);
  const [currentPage, setCurrentPage] = useState(getCurrentPage());
  const [totalItems, setTotalItems] = useState(1);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const setContextProps = useContextProps();
  const defaultPageSize = Number.parseInt(localStorage.getItem("pages:projects-list") ?? 30);

  const [modal, setModal] = React.useState(false);
  const openModal = setModal.bind(null, true);
  const closeModal = setModal.bind(null, false);

  const config = useConfig();
  useEffect(() => {
    // Retrieve the selected language from local storage or config when the component mounts
    const storedLanguage = localStorage.getItem('selectedLanguage');
    const configLanguage = config.language;
    if (configLanguage) {
      setSelectedLanguage(configLanguage);
    } else if (storedLanguage) {
      setSelectedLanguage(storedLanguage);
    }
  }, []);

  useEffect(() => {
    config.update({
      language: selectedLanguage,
      languageLocalCode: languages.find((language) => language.name === selectedLanguage)?.code
    });
  }, [selectedLanguage]);

  const fetchProjects = async (page = currentPage, pageSize = defaultPageSize) => {
    setNetworkState("loading");
    abortController.renew(); // Cancel any in flight requests




    const fetchAllProjects = async () => {
      setNetworkState("loading");
      let allProjects = [];
      let page = 1;
      const pageSize = 1000; // Set a large page size to minimize the number of requests

      while (true) {
        const requestParams = { page, page_size: pageSize };
        requestParams.include = [
          "id",
          "title",
          "created_by",
          "created_at",
          "color",
          "is_published",
          "assignment_settings",
          "description",
          "num_tasks_with_annotations",
          "task_number",
          "skipped_annotations_number",
          "total_annotations_number",
          "total_predictions_number",
          "ground_truth_number",
          "finished_task_number",
        ].join(",");
        const response = await api.callApi('projects', {
          params: requestParams,
          ...(isFF(FF_DEV_2575)
            ? {
              signal: abortController.controller.current.signal,
              errorFilter: (e) => e.error.includes("aborted"),
            }
            : null),
        });
        
        allProjects = allProjects.concat(response.results);

        if (!response.next) {
          break;
        }
        page += 1;
      }

      return allProjects;
    };

    const fetchProjectsByLanguage = async (language) => {
      const requestParams = { language };
      requestParams.include = [
        "id",
        "title",
        "created_by",
        "created_at",
        "color",
        "is_published",
        "assignment_settings",
        "description",
        "num_tasks_with_annotations",
        "task_number",
        "skipped_annotations_number",
        "total_annotations_number",
        "total_predictions_number",
        "ground_truth_number",
        "finished_task_number",
      ].join(",");
      const response = await api.callApi('projectsByLanguage', {
        // Page and page_size are not needed here, as we are fetching all projects for a language
        params: requestParams,
        ...(isFF(FF_DEV_2575)
          ? {
            signal: abortController.controller.current.signal,
            errorFilter: (e) => e.error.includes("aborted"),
          }
          : null),
      });
      // const response = await fetch(`/api/projects/filter-by-language?language=${language}`);
      
      return response.results;
    };

    let data;
    if (!selectedLanguage || selectedLanguage === "All" || selectedLanguage === '') {
      data = await fetchAllProjects();
    } else {
      data = await fetchProjectsByLanguage(selectedLanguage);
    }


    setTotalItems(data?.count ?? 1);
    setProjectsList(data ?? []);
    setNetworkState("loaded");

  };

  const loadNextPage = async (page, pageSize) => {
    setCurrentPage(page);
    await fetchProjects(page, pageSize);
  };

  React.useEffect(() => {
    if (selectedLanguage) {
      fetchProjects();
    }
  }, [selectedLanguage]);

  React.useEffect(() => {
    // there is a nice page with Create button when list is empty
    // so don't show the context button in that case
    setContextProps({ openModal, showButton: projectsList.length > 0 });
  }, [projectsList.length]);

  useEffect(() => {
    console.log('selectedLanguage changed', selectedLanguage);
  }, [selectedLanguage]);

  return (
    <Block name="projects-page">
      {(!selectedLanguage || selectedLanguage.length < 3) && (<ProjectLanguageSelector setSelectedLanguage={setSelectedLanguage} />)}
      <Oneof value={networkState}>
        <Elem name="loading" case="loading">
          <Spinner size={64} />
        </Elem>
        <Elem name="content" case="loaded">
          <ProjectsList
            projects={projectsList}
            currentPage={currentPage}
            totalItems={totalItems}
            loadNextPage={loadNextPage}
            pageSize={defaultPageSize}
            selectedLanguage={selectedLanguage}
          />
          {modal && <CreateProject onClose={closeModal} />}
        </Elem>
      </Oneof>
    </Block>
  );
};

ProjectsPage.title = "Projects";
ProjectsPage.path = "/projects";
ProjectsPage.exact = true;
ProjectsPage.routes = ({ store }) => [
  {
    title: () => store.project?.title,
    path: "/:id(\\d+)",
    exact: true,
    component: () => {
      const params = useRouterParams();

      return <Redirect to={`/projects/${params.id}/data`} />;
    },
    pages: {
      DataManagerPage,
      SettingsPage,
    },
  },
];
ProjectsPage.context = ({ openModal, showButton }) => {
  if (!showButton) return null;
  return (
    <Button onClick={openModal} look="primary" size="compact">
      Create
    </Button>
  );
};
