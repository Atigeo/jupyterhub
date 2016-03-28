FROM jupyter/singleuser
USER root
RUN apt-get update
RUN apt-get -y install r-base
RUN  apt-get install -y libzmq3-dbg libzmq3-dev libzmq3


ADD install.R /home/jovyan/
RUN echo 'options("repos"="http://cran.rstudio.com")' >> /usr/lib/R/etc/Rprofile.site

RUN Rscript -e "install.packages(c('rzmq','repr','IRkernel','IRdisplay'), repos = c('http://irkernel.github.io/', getOption('repos')))" -e "IRkernel::installspec()"


USER jovyan
RUN Rscript /home/jovyan/install.R

CMD ["sh", "/srv/singleuser/singleuser.sh"]
