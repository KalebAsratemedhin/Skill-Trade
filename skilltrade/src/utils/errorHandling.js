export const handleErrors = (error, customMessage) => {
    if (error.response && error.response.data) {
        const errorMessages = Object.keys(error.response.data).map(key => {
            return `${key}: ${error.response.data[key]}`;
          });
    
          console.log('Error messages:', errorMessages);
        
        throw new Error(errorMessages.join(' | '));
      }
  
      throw new Error(customMessage);
}