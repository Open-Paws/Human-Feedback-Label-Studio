import React, { useState } from 'react';
import { Modal, Button } from 'antd';

const LanguageModal = () => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
	setIsModalVisible(true);
  };

  const handleOk = () => {
	setIsModalVisible(false);
  };

  const handleCancel = () => {
	setIsModalVisible(false);
  };

  return (
	<div>
	  <Button type="primary" onClick={showModal}>
		Open Modal
	  </Button>
	  <Modal
		title="My Modal"
		visible={isModalVisible}
		onOk={handleOk}
		onCancel={handleCancel}
	  >
		<p>Some contents...</p>
	  </Modal>
	</div>
  );
};

export default LanguageModal;