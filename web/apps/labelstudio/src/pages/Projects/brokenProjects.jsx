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
  const [selectedLanguage, setSelectedLanguage] = useState();
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
      language:selectedLanguage, 
      languageLocalCode: languages.find((language) => language.name === selectedLanguage)?.code });
  }, [selectedLanguage]);



  const fetchProjects = async (page = currentPage, pageSize = defaultPageSize) => {
    setNetworkState("loading");
    abortController.renew(); // Cancel any in flight requests
    const requestParams = { page, page_size: pageSize };

    
      requestParams.include = [
        "id",
        "title",
        "created_by",
        "created_at",
        "color",
        "is_published",
        "assignment_settings",
      ].join(",");
    

    const fetchAllProjects = async () => {
      let allProjects = [];
      let page = 1;
    
      while (true) {
        const response = await fetch(`/api/projects?page=${page}&pageSize=${pageSize}&include=${requestParams.include}`);
        const data = await response.json();
        allProjects = allProjects.concat(data.results);
    
        if (!data.next) {
          break;
        }
        page += 1;
      }
    
      return allProjects;
    };

    const fetchProjectsByLanguage = async (language) => {
      let page = 1;
      
      const response = await fetch(`/api/projects/filter-by-language?language=${language}&page=${page}&pageSize=${pageSize}&include=${requestParams.include}`);
      const data = await response.json();
      return data.results;
    };

    let data;
    if (selectedLanguage === "All") {
      data = await fetchAllProjects();
    } else {
      data = await fetchProjectsByLanguage(selectedLanguage);
    } 

    if (data?.length) {
      const additionalData = await api.callApi("projects", {
        params: {
          ids: data?.map(({ id }) => id).join(","),
          include: [
            "id",
            "description",
            "num_tasks_with_annotations",
            "task_number",
            "skipped_annotations_number",
            "total_annotations_number",
            "total_predictions_number",
            "ground_truth_number",
            "finished_task_number",
          ].join(","),
          page_size: pageSize,
        },
        signal: abortController.controller.current.signal,
        errorFilter: (e) => e.error.includes("aborted"),
      });

      if (additionalData?.results?.length) {
        const mergedData = data.map((project) => {
          const additionalProject = additionalData.results.find(({ id }) => id === project.id);
          return {
            ...project,
            ...additionalProject,
          };
        });
        setProjectsList(mergedData);
      } else {
        setProjectsList(data);
      }
    }

    console.log('data ',data);

    setTotalItems(data?.count ?? 1);
    // setProjectsList(data ?? []);
    setNetworkState("loaded");

    // if (isFF(FF_DEV_2575) && data?.results?.length) {
    //   const additionalData = await api.callApi("projects", {
    //     params: {
    //       ids: data?.results?.map(({ id }) => id).join(","),
    //       include: [
    //         "id",
    //         "description",
    //         "num_tasks_with_annotations",
    //         "task_number",
    //         "skipped_annotations_number",
    //         "total_annotations_number",
    //         "total_predictions_number",
    //         "ground_truth_number",
    //         "finished_task_number",
    //       ].join(","),
    //       page_size: pageSize,
    //     },
    //     signal: abortController.controller.current.signal,
    //     errorFilter: (e) => e.error.includes("aborted"),
    //   });

    //   if (additionalData?.results?.length) {
    //     setProjectsList((prev) =>
    //       additionalData.results.map((project) => {
    //         const prevProject = prev.find(({ id }) => id === project.id);

    //         return {
    //           ...prevProject,
    //           ...project,
    //         };
    //       }),
    //     );
    //   }
    // }
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

  return (
    <Block name="projects-page">
      {!selectedLanguage ? (<ProjectLanguageSelector setSelectedLanguage={setSelectedLanguage} />
       ) : (
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
      )}
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
