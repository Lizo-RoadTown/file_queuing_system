FROM continuumio/miniconda3:latest

WORKDIR /workspace

# Copy the conda environment spec
COPY .devcontainer/env.yml /tmp/env.yml

# Create the environment and clean up to keep image size down
RUN conda env create -f /tmp/env.yml && \
    conda clean -afy

# Make the environment activate automatically in every shell session
RUN echo "conda activate epi-sde" >> ~/.bashrc

# Add the environment's Python to PATH so VS Code picks it up immediately
ENV PATH=/opt/conda/envs/epi-sde/bin:$PATH
ENV CONDA_DEFAULT_ENV=epi-sde
